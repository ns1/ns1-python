from ns1.rest.datasets import Datasets


class DatasetException(Exception):
    pass


class Dataset(object):
    """
    High level object representing a dataset.
    """

    def __init__(self, config):
        """
        Create a new high level Dataset object
        :param ns1.config.Config config: config object
        """
        self._rest = Datasets(config)
        self.config = config
        self.data = None

    def __repr__(self):
        return "<Dataset [%s]=%s,%s,%s,%s,%s,%s>" % (
            self.__getitem__("id"),
            self.__getitem__("name"),
            self.__getitem__("datatype"),
            self.__getitem__("repeat"),
            self.__getitem__("timeframe"),
            self.__getitem__("export_type"),
            self.__getitem__("recipient_emails"),
        )

    def __getitem__(self, item: str):
        if not self.data:
            raise DatasetException("dataset not loaded")
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload dataset data from the API.
        :param callback: function call back once the call has completed
        :param errback: function call back if the call fails
        """
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, id: str = None, callback=None, errback=None, reload=False):
        """
        Load dataset data from the API.
        :param str id: dataset id to load
        :param callback: function call back once the call has completed
        :param bool reload: whether to reuse the instance data instead of fetching it from the server
        """
        if not reload and self.data:
            return self.data
        if id is None and self.data:
            id = self.__getitem__("id")
        if id is None:
            raise DatasetException("no dataset id: did you mean to create?")

        def success(result: dict, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(id, callback=success, errback=errback)

    def loadFromDict(self, dt: dict):
        """
        Load dataset data from a dictionary.
        :param dict dt: dictionary containing *at least* either an id or domain/path/target
        """
        if "id" in dt or (
            "name" in dt
            and "datatype" in dt
            and "repeat" in dt
            and "timeframe" in dt
            and "export_type" in dt
            and "recipient_emails" in dt
        ):
            self.data = dt
            return self
        else:
            raise DatasetException("insufficient parameters")

    def delete(self, callback=None, errback=None):
        """
        Delete the dataset.
        :param callback: function call back once the call has completed
        :param errback: function call back if the call fails
        """
        id = self.__getitem__("id")
        return self._rest.delete(id, callback=callback, errback=errback)

    def create(
        self,
        name: str,
        datatype: dict,
        repeat: dict,
        timeframe: dict,
        export_type: str,
        recipient_emails: list,
        callback=None,
        errback=None,
        **kwargs
    ):
        """
        Create a new dataset. Pass a list of keywords and their values to
        configure. For the list of keywords available for dataset configuration,
        see :attr:`ns1.rest.datasets.Datasets.PASSTHRU_FIELDS`
        :param str name: the name of the dataset
        :param str datatype: datatype settings to define the type of data to be pulled
        :param str repeat: repeat settings to define recurrent reports
        :param str timeframe: timeframe settings for the data to be pulled
        :param str export_type: output format of the report
        :param str recipient_emails: list of user emails that will receive a copy of the report
        :param callback: function call back once the call has completed
        :param errback: function call back if the call fails
        """
        if self.data:
            raise DatasetException("dataset already loaded")

        return self._rest.create(
            name,
            datatype,
            repeat,
            timeframe,
            export_type,
            recipient_emails,
            callback=callback,
            errback=errback,
            **kwargs
        )

    def listDatasets(self, callback=None, errback=None):
        """
        Lists all datasets currently configured.
        :param callback: function call back once the call has completed
        :param errback: function call back if the call fails
        :return: a list of Dataset objects
        """

        def success(result, *args):
            ret = []
            for dt in result:
                ret.append(Dataset(self.config).loadFromDict(dt))
            if callback:
                return callback(ret)
            else:
                return ret

        return Datasets(self.config).list(callback=success, errback=errback)

    def retrieveReport(
        self, rp_id: str, dt_id: str = None, callback=None, errback=None
    ):
        """
        Retrieves a generated report given a dataset id and a report id
        :param str rp_id: the id of the generated report to download
        :param str dt_id: the id of the dataset that the above report belongs to
        :param callback: function call back once the call has completed
        :param errback: function call back if the call fails
        :return: generated report
        """

        if dt_id is None and self.data:
            dt_id = self.__getitem__("id")
        if dt_id is None:
            raise DatasetException("no dataset id: did you mean to create?")

        return Datasets(self.config).retrieveReport(
            dt_id, rp_id, callback=callback, errback=errback
        )
