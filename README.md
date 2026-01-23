HUD для хп/маны/валюты

- В 'TexturePaths' добавлены пути к ui‑текстурам (сердца, мана, медаль).
- В 'src/ui/hud.py' есть 'GameHUD' с методами 'display_health', 'display_mana', 'display_currency'.
- В 'base_projectile_test_room' HUD уже подключён и берёт хп/ману из игрока.

Как юзать ваще:
1. Создать 'GameHUD(self)' в окне и хранить в поле 'self.hud'.
2. В 'on_draw' после отрисовки мира вызвать:
   - 'self.gui_camera.use()'
   - 'self.hud.display_health(<текущее хп>)'
   - 'self.hud.display_mana(<текущая мана>)'
   - 'self.hud.display_currency(<валюта>)'
