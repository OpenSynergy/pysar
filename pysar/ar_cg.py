import jinja2

class CodeGen:
    def __init__(self, generator_name):
        self.generator_name = generator_name
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('templates'),
            trim_blocks=True)
        self.generator_template = self.template_env.get_template(self.generator_name)

    def generate(self, **kwargs):
        return self.generator_template.render(**kwargs)