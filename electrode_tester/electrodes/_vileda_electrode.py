from dataclasses import dataclass, field
from typing import Union, Dict, Tuple, List, Iterable
from ._base_electrode import BaseElectrode
from functools import cached_property

@dataclass(init=True, repr=True, frozen=True)
class ViledaElectrode(BaseElectrode):
    
    electrode_type:str = field(default='vileda', init=False)

    @cached_property
    def height(self):
        return self.normal_height - self.squeeze_height
        
    @cached_property
    def height_error(self):
        normal_height_error = (((self.height_delta ** 2) / 3) + self.normal_height_var)**.5
        squeeze_height_error = (((self.height_delta ** 2) / 3))**0.5
        
        return ((normal_height_error) ** 2 + (normal_height_error) ** 2)**.5