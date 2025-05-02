import logging

_logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='queries.log', 
    encoding='utf-8', 
    format='%(levelname)s:%(message)s',
    level=logging.INFO)


class QLogger:
    def add(self, search_type, task, params, query=None, collection=None, meth=None):
        if True: return
        _logger.info(
            f'{search_type}.{task}: {params}'
        )
        """ if query:
            self.add_explain(search_type, task, query)
        if collection is not None and meth == 1:
            _logger.info(
                f'{search_type}.{task}.explain: {getattr(collection.explain(), meth)(params)}'
            ) """

    def add_explain(self, search_type, task, query):
        _logger.info(
            f'{search_type}.{task}.explain: {query.explain()}'
        )