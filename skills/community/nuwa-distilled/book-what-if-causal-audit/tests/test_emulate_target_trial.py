from __future__ import annotations
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"emulate_target_trial.py"
BASE=['--question', 'Does A change Y?', '--population', 'eligible adults', '--treatment', 'strategy A', '--comparator', 'strategy B', '--outcome', 'Y at day 30', '--time-zero', 'eligibility day', '--follow-up', '30 days', '--estimand', 'risk difference', '--assumption', 'consistency', '--assumption', 'conditional exchangeability', '--assumption', 'positivity', '--evidence', 'registry v1']
def run(extra=None):
    return subprocess.run([sys.executable,str(SCRIPT),*BASE,*(extra or []),"--format","json"],text=True,capture_output=True)
class CliTests(unittest.TestCase):
    def test_deterministic_json(self):
        a,b=run(),run();self.assertEqual(a.returncode,0,a.stderr);self.assertEqual(a.stdout,b.stdout)
    def test_specific_shape_and_status(self):
        d=json.loads(run().stdout);self.assertIn("target_trial",d);self.assertEqual(d["epistemic_contract"]["status"],"design_and_assumption_audit_not_causal_proof")
    def test_provenance_claim_exists(self):
        d=json.loads(run().stdout);self.assertTrue(any("CIW025" in x["claim_ids"] for x in d["provenance"]))
    def test_blank_required_rejected(self):
        a=BASE.copy();i=a.index("--question")+1;a[i]="   ";p=subprocess.run([sys.executable,str(SCRIPT),*a],text=True,capture_output=True);self.assertEqual(p.returncode,2);self.assertIn("must not be blank",p.stderr)
    def test_duplicate_repeat_rejected(self):
        flag=next(x for x in BASE if x in ["--assumption","--loss","--user-group","--subject"]);v=BASE[BASE.index(flag)+1];p=run([flag,v]);self.assertEqual(p.returncode,2);self.assertIn("duplicate",p.stderr)
    def test_high_risk_missing_gates_fails(self):
        p=run(["--domain","personnel"]);self.assertEqual(p.returncode,2);self.assertIn("high-risk",p.stderr)
    def test_high_risk_complete_is_review_not_approval(self):
        p=run(["--domain","personnel",'--accountable-owner','owner','--applicable-rule','rule','--affected-group','workers','--impact-evidence','field audit v1','--appeal-path','independent review','--rollback-trigger','harm rises','--stop-condition','complaint threshold']);self.assertEqual(p.returncode,0,p.stderr);d=json.loads(p.stdout);self.assertEqual(d["safety_gate"]["status"],"governance_review_required");self.assertIn("submitted_not_verified",d["safety_gate"])
    def test_markdown_escapes_adversarial_text(self):
        a=BASE.copy();i=a.index("--question")+1;a[i]="<script>|x\\y";p=subprocess.run([sys.executable,str(SCRIPT),*a,"--format","markdown"],text=True,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertNotIn("<script>",p.stdout);self.assertIn("&lt;script&gt;",p.stdout);self.assertIn("\\|",p.stdout)
    def test_file_write(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"nested"/"audit.json";p=run(["--output",str(out)]);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(p.stdout,"");self.assertTrue(out.exists());json.loads(out.read_text())
    def test_output_does_not_claim_approval(self):
        d=json.loads(run().stdout);serialized=json.dumps(d);self.assertNotIn('"status": "approved"',serialized);self.assertIn("release_rule",d["safety_gate"])
if __name__=="__main__":unittest.main()
