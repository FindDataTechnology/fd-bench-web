# fd-bench-web

> **Part of the [Lex line (寻数·识律)](https://www.finddatatech.cloud/products/lex) of [FindData](https://www.finddatatech.cloud)** — the browser workbench for contract drafting and evaluation: clause corpus, taxonomy-driven assembly, LLM review, and a public read API.

See `PRODUCT.md` for what it is for and `DESIGN.md` for how it is put together.

## 跑起来

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # 产物在 dist/
```

## 目录

```
src/pages/index.astro    主工作台页面（条款语料、分类学装配、LLM 评审、公开读 API 的入口）
src/layouts/ src/styles/
bench-site-facts.json    站点对外声明的事实（产品口径、能力列表）
scripts/                 facts 生成与校验
reports/                 评测输出
```

## 三份文档的分工

| 文档 | 回答 |
|---|---|
| `PRODUCT.md` | 它是干什么的、给谁用 |
| `DESIGN.md` | 它是怎么搭起来的、为什么这么搭 |
| 本 README | 怎么跑起来、目录里有什么 |

## License

MIT — 见 `LICENSE`。
