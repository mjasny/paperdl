from .acm_org import ACMURLGenerator
from .ieee_org import IEEEURLGenerator
from .nejm_org import NEJMURLGenerator
from .sagepub_com import SagePubGenerator


SITES = [
    IEEEURLGenerator,
    ACMURLGenerator,
    NEJMURLGenerator,
    SagePubGenerator
]