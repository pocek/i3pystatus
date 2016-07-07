from i3pystatus import IntervalModule
from i3pystatus.core.command import run_through_shell

__author__ = 'facetoe'


class OpenVPN(IntervalModule):
    """
    Monitor OpenVPN connections.
    Currently only supports systems that use Systemd.

    Formatters:

    * {unit} — Same as setting.
    * {status} — Unicode up or down symbol.

    """

    color_up = "#00ff00"
    color_down = "#FF0000"
    status_up = '▲'
    status_down = '▼'
    format = "{unit} {status}"

    settings = (
        ("format", "Format string"),
        ("color_up", "VPN is up"),
        ("color_down", "VPN is down"),
        ("status_down", "Symbol to display when down"),
        ("status_up", "Symbol to display when up"),
        ("unit", "Systemd unit name"),
    )
    required = ("unit",)

    @property
    def active(self):
        command_result = run_through_shell(['systemctl', 'is-active', self.unit])
        return command_result.rc == 0

    def toggle(self):
        run_through_shell(['systemctl', 'stop' if self.active else 'start', self.unit])

    def run(self):
        if self.active:
            color = self.color_up
            status = self.status_up
        else:
            color = self.color_down
            status = self.status_down

        self.output = {
            "full_text": self.format.format(
                unit=self.unit,
                status=status),
            'color': color,
        }
