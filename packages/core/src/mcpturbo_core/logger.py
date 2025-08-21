"""Logging, tracing and metrics utilities for mcpturbo."""

from __future__ import annotations

import logging
from typing import Optional

import structlog
from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configure_logging(level: int = logging.INFO) -> None:
    """Configure structlog with JSON renderer."""

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(level=level)


def get_logger(name: str, request_id: Optional[str] = None):
    """Return a structlog logger optionally bound with a request_id."""

    logger = structlog.get_logger(name)
    if request_id is not None:
        logger = logger.bind(request_id=request_id)
    return logger


_tracer_provider: Optional[TracerProvider] = None


def init_tracing() -> TracerProvider:
    """Initialize and configure the global TracerProvider."""

    global _tracer_provider
    if _tracer_provider is None:
        _tracer_provider = TracerProvider()
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        _tracer_provider.add_span_processor(processor)
        trace.set_tracer_provider(_tracer_provider)
    return _tracer_provider


_meter_provider: Optional[MeterProvider] = None


def init_metrics() -> MeterProvider:
    """Initialize and configure the global MeterProvider."""

    global _meter_provider
    if _meter_provider is None:
        exporter = ConsoleMetricExporter()
        reader = PeriodicExportingMetricReader(exporter)
        _meter_provider = MeterProvider(metric_readers=[reader])
        metrics.set_meter_provider(_meter_provider)
    return _meter_provider


__all__ = [
    "configure_logging",
    "get_logger",
    "init_tracing",
    "init_metrics",
]

