#!/usr/bin/env python3
import argparse
import os
import traceback

import yaml
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3Format, B3MultiFormat
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from milo.cast import Cast
from milo.message import print_error
from milo.milobella import Milobella, MILOBELLA_TOKEN_ENV
from milo.run import run
from milo.stt.google import GoogleSTT
from milo.tracing.tracing import WithTracingSTT, WithTracingTTS, WithTracingWUW
from milo.tts.google2 import GoogleTTS2
from milo.wuw.__interface__ import WUWFeedbackInterface
from milo.wuw.pocketsphinx import PocketSphinxWUW


class PocketSphinxArguments:
    threshold: float


class Arguments:
    verbose: bool
    milobella_url: str
    plex_url: str
    plex_token: str
    keyword: str
    gpio_led: int
    pocketsphinx: PocketSphinxArguments
    tracing_config: dict


def validate_environment() -> None:
    if MILOBELLA_TOKEN_ENV not in os.environ:
        print_error(f"Missing env variable \"{MILOBELLA_TOKEN_ENV}\".")


def parse_arguments() -> Arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--url", help="Milobella URL", default="https://milobella.com:10443")
    parser.add_argument("--plex-url", help="Plex URL", default=None)
    parser.add_argument("--plex-token", help="Plex Token", default=None)
    parser.add_argument("--keyword", help="Wake up word", default="bella")
    parser.add_argument("--pocket-sphinx-threshold", help="Pocket Sphinx threshold", default=1e-30, type=float)
    parser.add_argument("--gpio-led", help="GPIO Led ID", default=-1, type=int)
    parser.add_argument("--tracing-config", default=None, type=argparse.FileType('r'),
                        help="Tracing YAML configuration file")

    args = parser.parse_args()
    args_obj = Arguments()
    args_obj.verbose = not not args.verbose
    args_obj.milobella_url = args.url
    args_obj.plex_url = args.plex_url
    args_obj.plex_token = args.plex_token
    args_obj.keyword = args.keyword
    args_obj.gpio_led = args.gpio_led
    psphinx_args = PocketSphinxArguments()
    psphinx_args.threshold = args.pocket_sphinx_threshold
    args_obj.pocketsphinx = psphinx_args
    if args.tracing_config:
        args_obj.tracing_config = yaml.load(args.tracing_config)

    return args_obj


def init_tracer(cfg: dict) -> None:
    provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: cfg["service_name"]})
    )
    jaeger_exporter = JaegerExporter(**cfg["jaeger"])
    provider.add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    trace.set_tracer_provider(provider)
    RequestsInstrumentor().instrument()
    set_global_textmap(B3MultiFormat())


def main():
    args = parse_arguments()
    validate_environment()
    init_tracer(args.tracing_config)

    # Technologies selection.
    tts = WithTracingTTS(GoogleTTS2())
    wuw = WithTracingWUW(PocketSphinxWUW(keyword=args.keyword, kws_threshold=args.pocketsphinx.threshold))
    stt = WithTracingSTT(GoogleSTT())

    wuw_feedback = WUWFeedbackInterface()
    if args.gpio_led >= 0:
        from milo.wuw.rpi_feedback import RPIWUWFeedback
        wuw_feedback = RPIWUWFeedback(args.gpio_led)

    cast = Cast(args.plex_url, args.plex_token)
    cast.start_discovery()

    # Initialize the milobella client
    milobella = Milobella(args.milobella_url, cast)

    # noinspection PyBroadException
    try:
        run(milobella, tts, wuw, stt, wuw_feedback)
    except Exception:
        print_error(traceback.format_exc())


if __name__ == "__main__":
    main()
