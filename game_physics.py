from game_utils import merge_numbers, min_max

class Direction:
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    DIR_NAMES = {
        LEFT : "Left",
        RIGHT : "Right",
        UP : "Up",
        DOWN : "Down",
        NONE : "None"
    }

class Force:
    FORCE_MAX = 10

    def __init__(self) -> None:
        self.force_left = 0
        self.force_right = 0
        self.force_up = 0
        self.force_down = 0

        self.lifespan = -1

    def __str__(self) -> str:
        return f"Force < {self.force_left}l {self.force_right}r {self.force_up}u {self.force_down}d >"

    def clear(self):
        self.force_left = 0
        self.force_right = 0
        self.force_up = 0
        self.force_down = 0       

    def apply_bounce(self, axis : str):
        if axis == "x":
            t_force = self.force_left
            self.force_left = self.force_right
            self.force_right = t_force
        if axis == "y":
            t_force = self.force_up
            self.force_up = self.force_down
            self.force_down = t_force

    def set_force(self, value, direction):
        if value > self.FORCE_MAX:
            value = self.FORCE_MAX

        match (direction):
            case Direction.LEFT:
                self.force_left = value
            case Direction.RIGHT:
                self.force_right = value
            case Direction.UP:
                self.force_up = value
            case Direction.DOWN:
                self.force_down = value

    def apply_force(self, value, direction):
        match (direction):
            case Direction.LEFT:
                value = max(self.force_left + value, 0)
            case Direction.RIGHT:
                value = max(self.force_right + value, 0)
            case Direction.UP:
                value = max(self.force_up + value, 0)
            case Direction.DOWN:
                value = max(self.force_down + value, 0)

        return self.set_force(value, direction)

    def total_force(self, force, minimum=0.1):
        tf = abs(force)
        if not force:
            return minimum
        
        return force / 2


class Velocity:
    V_MAX = 10

    def __init__(self) -> None:
        self.x_velocity = 0
        self.y_velocity = 0

        self.friction = 0
        self.bounce = False

    def __str__(self) -> str:
        return f"Velocity < {self.x_velocity} {self.y_velocity} >"

    def set_friction(self, value):
        self.friction = value

    def set_bounce(self, bounce : bool):
        self.bounce = bounce

    def apply_bounce(self, axis : str):
        if axis == "x":
            self.x_velocity = -self.x_velocity
        if axis == "y":
            self.y_velocity = -self.y_velocity

    def set_velocity(self, value, direction):
        match (direction):
            case Direction.LEFT:
                self.x_velocity = min_max(-self.V_MAX, self.x_velocity - value , self.V_MAX)
            case Direction.RIGHT:
                self.x_velocity = min_max(-self.V_MAX, self.x_velocity + value, self.V_MAX)
            case Direction.UP:
                self.y_velocity = min_max(-self.V_MAX, self.y_velocity - value, self.V_MAX)
            case Direction.DOWN:
                self.y_velocity = min_max(-self.V_MAX, self.y_velocity + value, self.V_MAX)

    def apply_velocity(self, value, direction):
        return self.set_velocity(value, direction)

    def _apply_force(self, force : Force):
        self.set_velocity(force.force_right, Direction.RIGHT)
        self.set_velocity(force.force_left, Direction.LEFT)
        self.set_velocity(force.force_up, Direction.UP)
        self.set_velocity(force.force_down, Direction.DOWN)

        if force.lifespan == 0:
            force.clear()
        elif force.lifespan > 0:
            force.lifespan -= 1
        
    def apply_forces(self, forces : list):
        for force in forces:
            self._apply_force(force)

        # Apply friction
        if self.friction == 0:
            return

        if self.x_velocity > 0:
            self.x_velocity = max(self.x_velocity - self.friction, 0)
        elif self.x_velocity < 0:
            self.x_velocity = min(self.x_velocity + self.friction, 0)

        if self.y_velocity > 0:
            self.y_velocity = max(self.y_velocity - self.friction, 0)
        elif self.y_velocity < 0:
            self.y_velocity = min(self.y_velocity + self.friction, 0)

    def translate_rect(self, rect):
        return rect.move((self.x_velocity, self.y_velocity))


