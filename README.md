# Como o CO₂ está mudando a Terra

Site estático com gráficos de temperatura global, CO₂ atmosférico e emissões do ano 0 até hoje.

## Como ver

```
cd site && python3 -m http.server 8000
```

Abra http://localhost:8000.

## Dados

`python3 scripts/build_data.py` baixa as séries modernas e gera `site/data.js`.
Os valores de 0–1849 (temperatura) e 0–1958 (CO₂) ficam em `data/*.csv` e são **aproximações** das reconstruções publicadas, boas para ver a tendência, não para citar números exatos.
