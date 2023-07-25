from typing import Optional
from text2phenotype.emr.datatypes import __vocabulary__

__vocab_to_coding_system = {v: k for k, v in __vocabulary__.items()}


def vocab_to_coding_system(vocab: str, default=None) -> Optional[str]:
    return __vocabulary__.get(vocab, default)


def coding_system_to_vocab(coding_system: str, default=None) -> Optional[str]:
    return __vocab_to_coding_system.get(coding_system, default)
