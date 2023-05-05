import random


class RequestData:

    def __init__(self, **kwargs):
        self.aspect_ratio = kwargs['aspect_ratio'] if 'aspect_ratio' in kwargs else 1
        self.easy_mode = kwargs['easy_mode'] if 'easy_mode' in kwargs else 'false'
        self.guidance_scale = kwargs['guidance_scale'] if 'guidance_scale' in kwargs else 7.5
        self.is_public = kwargs['is_public'] if 'is_public' in kwargs else 'false'
        self.model = kwargs['model'] if 'model' in kwargs else 'v2.1'
        self.negative_prompt = kwargs['negative_prompt'] if 'negative_prompt' in kwargs else ''
        self.num_inference_steps = kwargs['num_inference_steps'] if 'num_inference_steps' in kwargs else 50
        self.prompt = kwargs['prompt'] if 'prompt' in kwargs else ''
        self.seed = kwargs['seed'] if 'seed' in kwargs else self.__random_seed
        self.strength = kwargs['strength'] if 'strength' in kwargs else 0.8

    def __call__(self, *args, seed: bool | int | None = None, **kwargs):
        if isinstance(seed, int):
            self.seed = seed
        elif isinstance(seed, bool):
            self.seed = self.seed if seed else self.__random_seed
        else:
            self.seed = self.__random_seed
        return {"model": self.model,
                "guidance_scale": self.guidance_scale,
                "num_inference_steps": self.num_inference_steps,
                "aspect_ratio": self.aspect_ratio,
                "seed": self.seed,
                "strength": self.strength,
                "is_public": self.is_public,
                "easy_mode": self.easy_mode,
                "prompt": self.prompt,
                "negative_prompt": self.negative_prompt}

    @property
    def __random_seed(self) -> int:
        return int(random.random()*1e16)
