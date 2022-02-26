# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Medical Question Pairs dataset by McCreery et al (2020) contains pairs of medical questions and paraphrased versions of
the question prepared by medical professional.
"""

import os
from typing import Dict, Tuple
import datasets
from datasets import load_dataset


_CITATION = """\
@article{DBLP:journals/biodb/LiSJSWLDMWL16,
  author    = {Krallinger, M., Rabal, O., Lourenço, A.},
  title     = {Effective Transfer Learning for Identifying Similar Questions: Matching User Questions to COVID-19 FAQs},
  journal   = {KDD '20: Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining},
  volume    = {3458–3465},
  year      = {2020},
  url       = {https://github.com/curai/medical-question-pair-dataset},
  doi       = {},
  biburl    = {},
  bibsource = {}
}
"""

_DATASETNAME = "mqp"

_DESCRIPTION = """\
Medical Question Pairs dataset by McCreery et al (2020) contains pairs of medical questions and paraphrased versions of 
the question prepared by medical professional. Paraphrased versions were labelled as similar (syntactically dissimilar 
but contextually similar ) or dissimilar (syntactically may look similar but contextually dissimilar). Labels 1: similar, 0: dissimilar
"""

_HOMEPAGE = "https://biocreative.bioinformatics.udel.edu/tasks/biocreative-vi/track-5/"

_LICENSE = ""

_URLs = {"source": "https://raw.githubusercontent.com/curai/medical-question-pair-dataset/master/mqp.csv",
         "bigbio": "https://raw.githubusercontent.com/curai/medical-question-pair-dataset/master/mqp.csv"}

_SOURCE_VERSION = ""
_BIGBIO_VERSION = "1.0.0"


class MQPDataset(datasets.GeneratorBasedBuilder):
    """Medical Question Pairing dataset"""

    VERSION = datasets.Version(_SOURCE_VERSION)
    BIGBIO_VERSION = datasets.Version(_BIGBIO_VERSION)

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="source",
            version=_SOURCE_VERSION,
            description="Source schema"
        ),

        datasets.BuilderConfig(
            name="bigbio",
            version=BIGBIO_VERSION,
            description="BigScience Biomedical schema",
        ),
    ]

    DEFAULT_CONFIG_NAME = "source"

    def _info(self):

        if self.config.name == "source":
            features = datasets.Features(
                {
                    "document_id": datasets.Value("string"),
                    "text_1": datasets.Value("string"),
                    "text_2": datasets.Value("string"),
                    "label": datasets.Value("string")
                }
            )

        # Using in pairs schema
        elif self.config.name == "bigbio":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "document_id": datasets.Value("string"),
                    "text_1": datasets.Value("string"),
                    "text_2": datasets.Value("string"),
                    "label": datasets.Value("string")
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": my_urls,
                    "split": "train",
                }
            )
        ]

    def _generate_examples(self,
                           filepath,
                           split):
        """Yields examples as (key, example) tuples."""
        ds_dict = load_dataset('csv', delimiter=',',
                                column_names=["document_id", "text_1", "text_2", "label"],
                               data_files=filepath)

        if self.config.name == "source":
            for id_, (split, dataset) in enumerate(ds_dict.items()):
                yield id_, {
                    "document_id": dataset["document_id"][id_],
                    "text_1": dataset["text_1"][id_],
                    "text_2": dataset["text_2"][id_],
                    "label": dataset["label"][id_],
                }

        elif self.config.name == "bigbio":
            # global id (uid) starts from 1
            uid = 0
            for id_, (split, dataset) in enumerate(ds_dict.items()):
                uid += 1
                yield id_, {
                    "id": uid,
                    "document_id": dataset["document_id"][id_],
                    "text_1": dataset["text_1"][id_],
                    "text_2": dataset["text_2"][id_],
                    "label": dataset["label"][id_],
                }
                