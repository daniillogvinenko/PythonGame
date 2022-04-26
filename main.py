import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.25 # 0.09
TILE_SCALING = 0.5

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64

PLAYER_SIDE_SPEED = 5   # 5-9

JUMP_MAX_HEIGHT = 300  # 300-700

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.player_list = None
        self.background_list = None

        self.background_sprite1 = None
        self.background_sprite2 = None
        self.background_sprite3 = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # fluent movements
        self.keyLeftIsPressed = False

        self.keyRightIsPressed = False

        self.keyUpIsPressed = False

        self.camera = None

        self.current_gravity = None

        self.jumpSpeed = 40

        self.current_height = None

        # arcade.set_background_color(arcade.csscolor.ALICE_BLUE)

    # function checking if the player is inside the wall or not
    def isinside(self, player_sprite):
        for objectWall in self.wall_list:
            s_oy = abs(self.player_sprite.center_y - objectWall.center_y)
            min_sum_height = objectWall.width / 2 + PLAYER_WIDTH / 2
            if s_oy < min_sum_height:
                s_ox = abs(self.player_sprite.center_x - objectWall.center_x)
                min_sum_width = objectWall.height / 2 + PLAYER_HEIGHT / 2
                if s_ox < min_sum_width:
                    return True
        return False

    # есть ли снизу объект wall
    def iswallunder(self):
        for objectWall in self.wall_list:
            s_ox = abs(self.player_sprite.center_x - objectWall.center_x)
            min_sum_width = objectWall.width / 2 + PLAYER_WIDTH / 2
            if s_ox < min_sum_width:
                s_oy = self.player_sprite.center_y - objectWall.center_y
                min_sum_height = objectWall.height / 2 + PLAYER_HEIGHT / 2
                if s_oy < min_sum_height:
                    return False
        return True

    # есть ли справа объект wall
    def iswalltotheright(self):
        for objectWall in self.wall_list:
            s_oy = abs(self.player_sprite.center_y - objectWall.center_y)
            min_sum_height = objectWall.height / 2 + PLAYER_HEIGHT / 2
            if s_oy < min_sum_height-10:
                s_ox = objectWall.center_x - self.player_sprite.center_x
                min_sum_width = objectWall.width / 2 + PLAYER_WIDTH / 2
                if min_sum_width < s_ox and abs(s_ox < 10+min_sum_width):
                    return True
        return False

    # есть ли слева объект wall
    def iswalltotheleft(self):
        for objectWall in self.wall_list:
            s_oy = abs(self.player_sprite.center_y - objectWall.center_y)
            min_sum_height = objectWall.height / 2 + PLAYER_HEIGHT / 2

            if s_oy < min_sum_height-10:

                s_ox = self.player_sprite.center_x - objectWall.center_x
                min_sum_width = objectWall.width / 2 + PLAYER_WIDTH / 2
                if min_sum_width < s_ox and abs(s_ox < 10+min_sum_width):
                    return True
        return False

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.background_list = arcade.SpriteList(use_spatial_hash=True)

        # background




        self.background_sprite3 = arcade.Sprite("img/bg3.png", 1)
        self.background_sprite3.center_x = 2600
        self.background_sprite3.center_y = 543
        self.background_list.append(self.background_sprite3)

        self.background_sprite2 = arcade.Sprite("img/bg2.png", 1)
        self.background_sprite2.center_x = 2600
        self.background_sprite2.center_y = 543
        self.background_list.append(self.background_sprite2)

        self.background_sprite1 = arcade.Sprite("img/bg1.png", 1)
        self.background_sprite1.center_x = 2600
        self.background_sprite1.center_y = 543
        self.background_list.append(self.background_sprite1)


        self.camera = arcade.Camera(self.width,self.height)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "img/sprite4fall.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 75
        self.player_sprite.center_y = 96

        self.player_list.append(self.player_sprite)

        # активация гравитации
        self.current_gravity = True
        self.current_gravity_speed = 0

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 3000, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            wall.height = 64
            wall.width = 64
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96],[1000,100],[1000,200]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(":resources:images/tiles/brickGrey.png", TILE_SCALING)
            wall.center_x = coordinate[0]
            wall.center_y = coordinate[1]
            wall.height = 64
            wall.width = 64
            self.wall_list.append(wall)

        # red dot as an orient
        """self.red_dot = arcade.Sprite("img/reddot.png", 0.01)
        self.red_dot.center_x = 1000
        self.red_dot.center_y = 650
        self.wall_list.append(self.red_dot)"""

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here

        self.camera.use()

        # Draw our sprites
        self.background_list.draw()
        self.wall_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):

        """if self.iswallunder():
            self.player_sprite = arcade.Sprite("img/sprite4fall.png", CHARACTER_SCALING)
        else:
            self.player_sprite = arcade.Sprite("img/sprite1main.png", CHARACTER_SCALING)"""

        if self.keyLeftIsPressed and not self.iswalltotheleft():
            self.player_sprite.center_x -= PLAYER_SIDE_SPEED
        elif self.keyRightIsPressed and not self.iswalltotheright():
            self.player_sprite.center_x += PLAYER_SIDE_SPEED

        if self.keyLeftIsPressed and not self.iswalltotheleft() and self.player_sprite.center_x > SCREEN_WIDTH/2:
            self.background_sprite1.center_x -= PLAYER_SIDE_SPEED / 4
            self.background_sprite2.center_x -= PLAYER_SIDE_SPEED / 3
            self.background_sprite3.center_x -= PLAYER_SIDE_SPEED / 2
        elif self.keyRightIsPressed and not self.iswalltotheright() and self.player_sprite.center_x > SCREEN_WIDTH/2:
            self.background_sprite1.center_x += PLAYER_SIDE_SPEED / 4
            self.background_sprite2.center_x += PLAYER_SIDE_SPEED / 3
            self.background_sprite3.center_x += PLAYER_SIDE_SPEED / 2

        if self.keyUpIsPressed:
            if self.player_sprite.center_y < self.current_height + JUMP_MAX_HEIGHT:
                self.player_sprite.center_y += self.jumpSpeed
                if self.jumpSpeed > 15:
                    self.jumpSpeed -= 2
            else:
                self.player_sprite.center_y += JUMP_MAX_HEIGHT - (self.player_sprite.center_y - self.current_height)
                self.keyUpIsPressed = False
                self.jumpSpeed = 40

        # Position the camera
        self.center_camera_to_player()

        # activating gravity
        if self.current_gravity and self.iswallunder():
            self.player_sprite.center_y -= self.current_gravity_speed
            if self.current_gravity_speed < 8:
                self.current_gravity_speed += 1



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.keyLeftIsPressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.keyRightIsPressed = True
        elif (key == arcade.key.UP or key == arcade.key.W) and not self.iswallunder():
            self.keyUpIsPressed = True
            self.current_height = self.player_sprite.center_y
            self.jumpSpeed = 40
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.center_y -= 1

    """called when a key is released"""
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.keyLeftIsPressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.keyRightIsPressed = False


    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()