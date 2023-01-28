import enum


class RoleType(enum.Enum):
    user = "user"
    staff = "staff"
    admin = "admin"


class Status(enum.Enum):
    running = "running"
    stopped = "stopped"
    unstable = "unstable"
