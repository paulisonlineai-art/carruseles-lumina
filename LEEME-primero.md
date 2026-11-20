# Cómo usar el agente de carruseles en tu Mac

## Una sola vez
1. Descomprime `lumina-carruseles.zip` donde quieras, por ejemplo en `~/Documents/lumina-carruseles`.
2. Comprueba que tienes Claude Code (`claude --version`) y la extensión Claude in Chrome instalada y con sesión iniciada en Chrome.
3. Si `python3 -c "import PIL"` da error, instala Pillow con `pip3 install --user pillow`.

## Cada día
```
cd ~/Documents/lumina-carruseles
claude --chrome
```
Luego escribe:
```
/carruseles
```
También le puedes dar indicaciones: `/carruseles hoy enfócate en dormir y luna llena`.

- Tarda unos 15–25 minutos.
- Al terminar abre la carpeta `~/Downloads/Lumina-carruseles/<fecha>/` con los 6 zips y el archivo `publicar_hoy.md`, que trae las descripciones y los horarios.
- Mientras trabaja, Chrome tiene que estar abierto. El agente abre una pestaña propia de TikTok, solo lee y la cierra al terminar.

## Fotos nuevas
Pon fotos nuevas en `fotos/apoyo/` o `fotos/apoyo-sofia/`, con un nombre que describa la foto, por ejemplo `vela-libreta-noche.jpg`.

Si agregas fotos nuevas de Valu o de Sofi para portada, pídele en Claude Code: "agrega la cara de las fotos nuevas a caras.json". Sin ese dato, el script intenta centrar la cara solo.

## Más adelante: automático
Cuando la prueba salga bien, se puede programar para que corra solo cada mañana. Pídemelo y lo armamos.
