from torch import nn

from utils import settings_is_valid


class DQN(nn.Module):
    def __init__(self, settings):
        required_settings = ["num_actions"]
        if not settings_is_valid(settings, required_settings):
            raise Exception(
                f"Settings object {settings} missing some required settings."
            )

        super(DQN, self).__init__()

        self.num_actions = settings["num_actions"]

        # input size: N, 3, 84, 84
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=8, stride=4,),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(inplace=True),
        )
        # input size: N, 32, 20, 20
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(inplace=True),
        )
        # input size: N, 64, 9, 9
        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(inplace=True),
        )
        # input size: N, 64, 7, 7
        # After flattening: 1, 3136
        self.fc4 = nn.Linear(3136, 512, bias=True)
        self.relu4 = nn.LeakyReLU(inplace=True)
        # input size: N, 512
        self.fc5 = nn.Linear(512, self.num_actions, bias=True)
        self.log_softmax5 = nn.LogSoftmax(dim=1)
        # output size: N, num_actions

    def forward(self, x):
        """
        Parameters
        ----------
        x : np.array
            The state of the environment.

        Returns
        -------
        np.array
            A vector of Q(s, a) estimates for each possible action a.
        """
        # Convolutions
        out = self.conv1(x)
        out = self.conv2(out)
        out = self.conv3(out)
        # Flatten before passing to fc
        out = out.view(out.size()[0], -1)
        out = self.fc4(out)
        out = self.relu4(out)
        # Fully Connected
        out = self.fc5(out)
        out = self.log_softmax5(out)
        return out
