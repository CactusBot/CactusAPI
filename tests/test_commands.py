from json import dumps, loads


class TestCommands:
    url = "/api/v1/user/paradigmshift3d/command"
    data = {}

    def test_create(self, client, api_auth, command_data):
        """Valid command creation"""
        # Get data from the creation_data dict
        name = "foo"
        cmd = client.patch(self.url + "/" + name,
                           data=dumps(command_data[name]),
                           content_type="application/json",
                           headers=api_auth)

        data = loads(cmd.data.decode())["data"]
        assert data["attributes"]["count"] == 0
        del data["attributes"]["count"]
        del data["attributes"]["createdAt"]

        assert "attributes" in data
        assert "id" in data
        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"]["enabled"] is True
        assert data["attributes"]["name"] == name
        assert data["type"] == "command"

        # The submitted data does not have these keys and we already asserted
        # them, so add them so the final test can complete
        command_data[name]["token"] = data["attributes"]["token"]
        command_data[name]["enabled"] = data["attributes"]["enabled"]

        assert command_data[name] == data["attributes"]

    def test_single(self, client, command_data):
        """Get a single user object and see if it matches (it should)"""
        name = "foo"
        cmd = client.get(self.url + "/" + command_data[name]["name"])

        cmd_data = loads(cmd.data.decode())["data"]
        assert cmd_data["attributes"]["count"] == 0
        assert cmd_data["attributes"].get("enabled", False)
        assert cmd_data["attributes"]["token"] == "paradigmshift3d"
        # TODO: Check createdAt

        del cmd_data["attributes"]["count"]
        del cmd_data["attributes"]["token"]
        del cmd_data["attributes"]["enabled"]
        del cmd_data["attributes"]["createdAt"]

        assert cmd_data["attributes"] == command_data[name]

    def test_all(self, client, api_auth, command_data):
        # Create the second command
        name = "bar"
        cmd = client.patch(
            self.url + "/" + name,
            data=dumps(command_data[name]),
            content_type="application/json",
            headers=api_auth
        )
        cmd_create_data = loads(cmd.data.decode())["data"]

        assert "attributes" in cmd_create_data
        assert "id" in cmd_create_data
        assert cmd_create_data["attributes"]["token"] == "paradigmshift3d"
        assert cmd_create_data["attributes"]["enabled"] is True
        assert cmd_create_data["attributes"]["name"] == name
        assert cmd_create_data["type"] == "command"
        # TODO: Check createdAt

        # These have already been asserted, so go ahead and remove them
        del cmd_create_data["attributes"]["count"]
        del cmd_create_data["attributes"]["enabled"]
        del cmd_create_data["attributes"]["token"]
        del cmd_create_data["attributes"]["createdAt"]

        assert cmd_create_data["attributes"] == command_data[name]

        cmd = client.get(self.url)
        cmd_all_data = loads(cmd.data.decode())["data"]
        assert len(cmd_all_data) == 2

        returned_cmds = [cmd["attributes"]["name"] for cmd in cmd_all_data]

        for name in command_data.keys():
            if name not in returned_cmds:
                raise AssertionError(
                    "Command {name} was not returned by API!".format(name=name)
                )

    def test_edit(self, client, api_auth):
        edit_data = {
            "enabled": False,
            "response": {
                "message": [
                    {
                        "type": "emoji",
                        "data": "smile",
                        "text": ":)"
                    }
                ]
            }
        }
        edit_name = "foo"

        cmd = client.patch(
            self.url + "/" + edit_name,
            data=dumps(edit_data),
            content_type="application/json",
            headers=api_auth
        )

        data = loads(cmd.data.decode())

        assert data["meta"]["edited"] is True
        assert data["data"]["attributes"]["enabled"] is False
        assert data["data"]["attributes"][
            "response"]["message"] == edit_data["response"]["message"]

    def test_removal(self, client, api_auth, command_data):
        """Remove a command and see if it matches"""
        # Using the quote ID from the first created quote
        for name in command_data.keys():
            _ = client.delete(self.url + "/" + name, headers=api_auth)

        # Create command to delete
        name = "foo"
        cmd = client.patch(self.url + "/" + name,
                           data=dumps(command_data[name]),
                           content_type="application/json",
                           headers=api_auth)

        created_id = loads(cmd.data.decode())["data"]["id"]

        deleted = client.delete(self.url + "/" + name, headers=api_auth)
        deletion_data = loads(deleted.data.decode())

        assert deletion_data["meta"]["deleted"]["command"][0] == created_id

    def test_alias_and_repeat_removal(self, client, api_auth,
                                      command_data, repeat_data, alias_data):
        name = "foo"
        cmd = client.patch(self.url + "/" + name,
                           data=dumps(command_data[name]),
                           content_type="application/json",
                           headers=api_auth)
        cmd_id = loads(cmd.data.decode())["data"]["id"]
        repeat = client.patch("/api/v1/user/paradigmshift3d/repeat/potato",
                              data=dumps(repeat_data["potato"]),
                              content_type="application/json",
                              headers=api_auth)
        repeat_id = loads(repeat.data.decode())["data"]["id"]
        alias = client.patch("/api/v1/user/paradigmshift3d/alias/test",
                             data=dumps(alias_data["test"]),
                             content_type="application/json",
                             headers=api_auth)
        alias_id = loads(alias.data.decode())["data"]["id"]
        deleted = client.delete(self.url + "/" + name, headers=api_auth)
        data = loads(deleted.data.decode())
        assert "meta" in data
        assert len(data["meta"]["deleted"]) == 3
        assert len(data["meta"]["deleted"]["command"]) == 1
        assert len(data["meta"]["deleted"]["repeats"]) == 1
        assert len(data["meta"]["deleted"]["aliases"]) == 1
        assert data["meta"]["deleted"]["command"][0] == cmd_id
        assert data["meta"]["deleted"]["repeats"][0] == repeat_id
        assert data["meta"]["deleted"]["aliases"][0] == alias_id

    def test_get_nonexistant(self, client, api_auth):
        # TODO Requests command that exists for another user but not token one
        pass
