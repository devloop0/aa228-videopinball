import time

import gym
import torch

from dqn import DQN
from utils import process_state


def load_model(model_filename, num_actions):
    settings = {"num_actions": num_actions}
    model = DQN(settings)
    model.load_state_dict(torch.load(model_filename))
    model.eval()
    return model


def load_model_checkpoint(checkpoint_filename, num_actions):
    settings = {"num_actions": num_actions}
    model = DQN(settings)
    model.load_state_dict(torch.load(checkpoint_filename)["model_state_dict"])
    model.eval()
    return model


def play_using_model(env, model, device, max_steps=10000):
    model.eval()
    with torch.no_grad():
        state = process_state(env.reset()).to(device)
        for step in range(max_steps):
            env.render()
            forward_res = model.forward(state)
            action = torch.argmax(forward_res, dim=1).item()
            state, reward, done, info = env.step(action)
            if step % 500 == 0:
                print("FORWARD_RES", forward_res)
                print("INFO", info)
                print("REWARD", reward)
            state = process_state(state).to(device)

            if done:
                break

            time.sleep(0.05)


if __name__ == "__main__":
    # Initialize environment
    env = gym.make("VideoPinball-v0")

    # Initialize model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    num_actions = env.action_space.n
    model = load_model("out/dqn.model", num_actions).to(device)

    # play using model
    play_using_model(env, model, device)
