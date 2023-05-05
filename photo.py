from requestdata import RequestData


class Photo:
    id: str
    url: str

    def __init__(self, data: dict):
        data = data['results'][0]
        self.id = data['id']
        self.uid = data['uid']
        self.width = data['width']
        self.height = data['height']
        self.blurhash = data['blurhash']
        self.is_nsfw = data['is_nsfw']
        self.is_public = data['is_public']
        self.enhanced = data['is_enhanced']
        self.tags = data['tags']
        self.model_name = data['model_name']
        self.model_version = data['model_version']
        self.created_at = data['created_at']
        self.num_inference_steps = data['metadata']['num_inference_steps']
        self.guidance_scale = data['metadata']['guidance_scale']
        self.prompt = data['metadata']['prompt']
        self.negative_prompt = data['metadata']['negative_prompt']
        self.seed = data['metadata']['seed']
        self.url = data['image_url']

    def __call__(self):
        data = RequestData(aspect_ratio=0.5625,
                           easy_mode='false',
                           guidance_scale=self.guidance_scale,
                           is_public='false',
                           model=self.model_version,
                           negative_prompt=self.negative_prompt,
                           num_inference_steps=self.num_inference_steps,
                           prompt=self.prompt,
                           seed=self.seed,
                           strength=0.8)
        return data()
