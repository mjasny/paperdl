from .acm_org import ACMURLGenerator
from .ieee_org import IEEEURLGenerator
from .nejm_org import NEJMURLGenerator


SITES = [IEEEURLGenerator, ACMURLGenerator, NEJMURLGenerator]