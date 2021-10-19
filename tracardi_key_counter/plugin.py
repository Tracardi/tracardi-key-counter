from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from tracardi.domain.profile import Profile

from tracardi_key_counter.model.configuration import Configuration
from tracardi_key_counter.service.key_counter import KeyCounter


def validate(config: dict) -> Configuration:
    return Configuration(**config)


class KeyCounterAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)

    async def run(self, payload):

        dot = self._get_dot_accessor(payload)

        # If path does not exist then create empty value
        if self.config.save_in not in dot:
            dot[self.config.save_in] = {}

        counter_dict = dot[self.config.save_in]

        if counter_dict is None:
            counter_dict = {}
        else:
            if not isinstance(counter_dict, dict):
                raise ValueError(f"Path [{self.config.save_in}] for key counting must be dict, "
                                 f"{type(counter_dict)} given.")

        if isinstance(self.config.key, list):
            keys_to_count = [dot[key] for key in self.config.key]
        else:
            keys_to_count = dot[self.config.key]

        # Save counts
        counter = KeyCounter(counter_dict)
        counter.count(keys_to_count)

        dot[self.config.save_in] = counter.counts

        self.profile.replace(Profile(**dot.profile))

        return Result(port='counts', value=counter.counts)


def register() -> Plugin:
    return Plugin(
        start=False,
        debug=False,
        spec=Spec(
            module='tracardi_key_counter.plugin',
            className='KeyCounterAction',
            inputs=['payload'],
            outputs=['counts'],
            version="0.6.0",
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "key": None,
                "save_in": None
            }
        ),
        metadata=MetaData(
            name='Key counter',
            desc='Counts keys and saves it in profile.',
            type='flowNode',
            width=200,
            height=100,
            icon='bar-chart',
            group=['Stats']
        )
    )
