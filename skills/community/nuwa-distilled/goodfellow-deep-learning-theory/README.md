# goodfellow-deep-learning-theory

Goodfellow/Bengio/Courville 理论主模块：假设→方程→计算图→梯度/优化→泛化失败→数值反证，并将 Transformer/LLM 明确列为 post-2016 补充。

```bash
python3 scripts/check_derivation.py --exercise finite-difference --x 0.7 --target 1 --step 1e-5 --output derivation.json
python3 -m unittest discover -s tests -v
```
