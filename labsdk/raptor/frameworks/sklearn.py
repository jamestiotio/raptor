# -*- coding: utf-8 -*-
#  Copyright (c) 2022 RaptorML authors.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from .base import BaseModelFramework


class SklearnFramework(BaseModelFramework):
    @staticmethod
    def save(model, spec: 'ModelSpec'):
        try:
            import joblib
            from sklearn import __version__ as sklearn_version
            from sklearn.base import BaseEstimator
        except ImportError:
            raise ImportError('Please install joblib and sklearn to use the sklearn framework.\n'
                              'You can install them using pip: `pip install joblib scikit-learn`')

        if not isinstance(model, BaseEstimator):
            raise TypeError('model must be a sklearn model')

        BaseModelFramework._create_output_path()
        spec._model_framework_version = sklearn_version

        base_filename = f'{spec.fqn()}_{model.__hash__()}.job'
        job_path = f'{BaseModelFramework._base_output_path()}/{base_filename}'
        joblib.dump(model, job_path)

        import shutil, os
        shutil.make_archive(job_path, 'gztar', BaseModelFramework._base_output_path())
        os.remove(job_path)
        spec._model_filename = f'{base_filename}.tar.gz'

    @staticmethod
    def predict(model, data):
        return model.predict(data)