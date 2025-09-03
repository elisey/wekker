# ABOUTME: Multi-stage ADC filtering implementation with hardware debouncing, moving average, and hysteresis
# ABOUTME: Provides stable, noise-free readings from analog sensors by wrapping any ADCReader implementation

import time
from collections import deque
from typing import Optional

from .adc_reader import ADCReader


class FilteredADCReader:
    """
    Multi-stage ADC filter that wraps any ADCReader implementation.
    
    Filtering pipeline:
    Stage 1: Hardware debouncing (delegated to wrapped ADC reader)
    Stage 2: Moving average filter (reduces noise)
    Stage 3: Hysteresis filter (prevents jitter)
    """
    
    # Class constants for configuration
    DEFAULT_BUFFER_SIZE = 2
    DEFAULT_HYSTERESIS_THRESHOLD = 2
    DEFAULT_FORBIDDEN_VALUES = {128, 192}
    DEFAULT_MAX_RETRIES = 15
    
    def __init__(self, adc_reader: ADCReader):
        """
        Initialize filtered ADC reader.
        
        Args:
            adc_reader: Underlying ADC reader implementation
        """
        self.adc_reader = adc_reader
        self.buffer_size = self.DEFAULT_BUFFER_SIZE
        self.hysteresis_threshold = self.DEFAULT_HYSTERESIS_THRESHOLD
        self.forbidden_values = self.DEFAULT_FORBIDDEN_VALUES
        self.max_retries = self.DEFAULT_MAX_RETRIES
        
        # Stage 2: Moving average buffer
        self.sample_buffer: deque[int] = deque(maxlen=self.buffer_size)
        
        # Stage 3: Hysteresis state
        self.last_output: Optional[int] = None
    
    def read_value(self) -> int:
        """
        Read filtered ADC value through 3-stage pipeline.
        
        Returns:
            int: Filtered ADC value in range 0-255
        """
        # Stage 1: Hardware debouncing
        debounced_value = self._apply_hardware_debouncing()
        
        # Stage 2: Moving average filter
        averaged_value = self._apply_moving_average(debounced_value)
        
        # Stage 3: Hysteresis filter
        filtered_value = self._apply_hysteresis(averaged_value)
        
        return filtered_value
    
    def _apply_hardware_debouncing(self) -> int:
        """
        Apply hardware debouncing by filtering out forbidden values.
        
        Reads from the underlying ADC reader multiple times until a valid value
        is obtained or max retries is reached.
        
        Returns:
            int: Hardware debounced ADC reading
        """
        value = 0
        counter = 0
        
        for _ in range(self.max_retries):
            value = self.adc_reader.read_value()
            if value not in self.forbidden_values:
                break
            counter += 1
            time.sleep(0.01 * counter)
        
        if value in self.forbidden_values:
            print(f"ADC: {value}")
        
        return value
    
    def _apply_moving_average(self, debounced_value: int) -> int:
        """
        Apply moving average filter to reduce noise.
        
        Args:
            debounced_value: Hardware debounced ADC reading
            
        Returns:
            int: Moving average of last N samples
        """
        # Add new sample to buffer
        self.sample_buffer.append(debounced_value)
        
        # Calculate average of all samples in buffer
        average = sum(self.sample_buffer) // len(self.sample_buffer)
        
        return average
    
    def _apply_hysteresis(self, averaged_value: int) -> int:
        """
        Apply hysteresis filter to prevent jitter around boundaries.
        
        Args:
            averaged_value: Moving average filtered value
            
        Returns:
            int: Hysteresis filtered value
        """
        # First reading - initialize output
        if self.last_output is None:
            self.last_output = averaged_value
            return averaged_value
        
        # Check if change exceeds hysteresis threshold
        change = abs(averaged_value - self.last_output)
        if change >= self.hysteresis_threshold:
            self.last_output = averaged_value
            return averaged_value
        
        # Change too small - return previous output
        return self.last_output
    
    def reset(self) -> None:
        """
        Reset filter state (clear buffers and hysteresis).
        """
        self.sample_buffer.clear()
        self.last_output = None