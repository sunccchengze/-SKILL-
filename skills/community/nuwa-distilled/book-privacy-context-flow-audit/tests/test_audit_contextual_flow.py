from __future__ import annotations
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"audit_contextual_flow.py"
BASE=['--context', 'university teaching', '--context-purpose', 'learning and fair assessment', '--subject', 'student', '--sender', 'teacher', '--recipient', 'assistant', '--attribute', 'grade', '--transmission-principle', 'confidential need to know', '--baseline-norm', 'teacher may share grade with course assistant in confidence', '--proposed-change', 'send grade to model vendor', '--norm-evidence', 'course policy v3']
def run(extra=None):
    return subprocess.run([sys.executable,str(SCRIPT),*BASE,*(extra or []),"--format","json"],text=True,capture_output=True)
class CliTests(unittest.TestCase):
    def test_deterministic_json(self):
        a,b=run(),run();self.assertEqual(a.returncode,0,a.stderr);self.assertEqual(a.stdout,b.stdout)
    def test_specific_shape_and_status(self):
        d=json.loads(run().stdout);self.assertIn("decision_heuristic",d);self.assertEqual(d["epistemic_contract"]["status"],"prima_facie_privacy_audit_not_legal_approval")
    def test_provenance_claim_exists(self):
        d=json.loads(run().stdout);self.assertTrue(any("PIC025" in x["claim_ids"] for x in d["provenance"]))
    def test_blank_required_rejected(self):
        a=BASE.copy();i=a.index("--context")+1;a[i]="   ";p=subprocess.run([sys.executable,str(SCRIPT),*a],text=True,capture_output=True);self.assertEqual(p.returncode,2);self.assertIn("must not be blank",p.stderr)
    def test_duplicate_repeat_rejected(self):
        flag=next(x for x in BASE if x in ["--assumption","--loss","--user-group","--subject"]);v=BASE[BASE.index(flag)+1];p=run([flag,v]);self.assertEqual(p.returncode,2);self.assertIn("duplicate",p.stderr)
    def test_high_risk_missing_gates_fails(self):
        p=run(["--domain","credit"]);self.assertEqual(p.returncode,2);self.assertIn("high-risk",p.stderr)
    def test_high_risk_complete_is_review_not_approval(self):
        p=run(["--domain","credit",'--accountable-owner','owner','--applicable-rule','rule','--affected-group','borrowers','--impact-evidence','field impact audit','--contest-path','independent correction review','--rollback-trigger','disparate harm','--stop-condition','complaint threshold']);self.assertEqual(p.returncode,0,p.stderr);d=json.loads(p.stdout);self.assertEqual(d["safety_gate"]["status"],"governance_review_required");self.assertIn("submitted_not_verified",d["safety_gate"])
    def test_markdown_escapes_adversarial_text(self):
        a=BASE.copy();i=a.index("--context")+1;a[i]="<script>|x\\y";p=subprocess.run([sys.executable,str(SCRIPT),*a,"--format","markdown"],text=True,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertNotIn("<script>",p.stdout);self.assertIn("&lt;script&gt;",p.stdout);self.assertIn("\\|",p.stdout)
    def test_file_write(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"nested"/"audit.json";p=run(["--output",str(out)]);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(p.stdout,"");self.assertTrue(out.exists());json.loads(out.read_text())
    def test_output_does_not_claim_approval(self):
        d=json.loads(run().stdout);serialized=json.dumps(d);self.assertNotIn('"status": "approved"',serialized);self.assertIn("release_rule",d["safety_gate"])
if __name__=="__main__":unittest.main()
