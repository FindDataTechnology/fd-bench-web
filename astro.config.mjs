import { defineConfig } from 'astro/config';

// 知验台分发链介绍站（add-bench-chain-website）。域名 bench.finddatatech.cloud。
// 静态构建（对齐 fd-qicai-web / fd-marketing-web 先例，Caddy file_server 直出 /opt/fd/bench-web/dist）；
// 「实时概况带」经浏览器 fetch 同源 /api/public/overview（生产由 Caddy 反代到 bench 公共 pod 同路径，
// 见 design D3/D4；水合失败如实报因，不做本地缓存）。
// 本地 dev 暂不配 vite proxy：上游 law-bench add-bench-public-overview-tier 的公共 pod
// 地址未定，端点 live 后在此补一段 '/api/public/overview' 代理即可；dev 下水合走报因态即真实。
export default defineConfig({
  site: 'https://bench.finddatatech.cloud',
});
