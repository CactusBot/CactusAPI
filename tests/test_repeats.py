"""Tests the repeat endpoint of the API"""
import json


class TestRepeats:
    """Tests the repeat endpoint of the API"""
    url = "/api/v1/user/paradigmshift3d/repeat"

    def test_create(self, client, api_auth, command_data, repeat_data):
        """Valid repeat creation"""
        name = "test"
        cmd_name = "foo"
        cmd = client.patch("/api/v1/user/paradigmshift3d/command/" + cmd_name,
                           data=json.dumps(command_data[cmd_name]),
                           content_type="application/json",
                           headers=api_auth)

        # The command was created successfully, so we can continue
        assert cmd.status_code == 201
        created_id = json.loads(cmd.data.decode())["data"]["id"]

        repeat = client.patch(self.url + '/' + name,
                              data=json.dumps(repeat_data[name]),
                              content_type="application/json",
                              headers=api_auth)
        data = json.loads(repeat.data.decode())["data"]
        assert repeat.status_code == 201
        assert data["type"] == "repeat"

        assert data["attributes"]["repeatName"] == name
        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"]["command"]["id"] == created_id
        assert data["attributes"][
            "commandName"] == repeat_data[name]["commandName"]
        assert data["attributes"][
            "period"] == repeat_data[name]["period"]

    def test_single(self, client, api_auth, repeat_data):
        """A test that does stuff, namely checking if stuff == other stuff"""
        name = "potato"

        repeat = client.patch(self.url + '/' + name,
                              data=json.dumps(repeat_data[name]),
                              content_type="application/json",
                              headers=api_auth)
        created_id = json.loads(repeat.data.decode())["data"]["id"]
        assert repeat.status_code == 201

        repeat = client.get(self.url + '/' + name)
        data = json.loads(repeat.data.decode())["data"]
        assert data["id"] == created_id
        assert data["attributes"]["repeatName"] == name
        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"][
            "commandName"] == repeat_data[name]["commandName"]
        assert data["attributes"][
            "period"] == repeat_data[name]["period"]

    def test_all(self, client, api_auth, repeat_data):
        repeats = client.get(self.url)
        assert repeats.status_code == 200
        data = json.loads(repeats.data.decode())["data"]

        assert len(data) == 2
        comparison = {
            repeat["attributes"]["repeatName"]: {
                "commandName": repeat["attributes"]["commandName"],
                "period": repeat["attributes"]["period"]
            } for repeat in data}
        assert repeat_data.items() == comparison.items()
        for repeat in data:
            assert repeat["type"] == "repeat"
        for repeat in repeat_data.keys():
            assert (client.delete(self.url + '/' + repeat,
                                  headers=api_auth)).status_code == 200

    def test_delete(self, client, api_auth, repeat_data):
        """Test to see if the services are being removed properly"""
        name = "potato"

        repeat = client.patch(self.url + '/' + name,
                              data=json.dumps(repeat_data[name]),
                              content_type="application/json",
                              headers=api_auth)
        created_id = json.loads(repeat.data.decode())["data"]["id"]
        assert repeat.status_code == 201

        deleted = client.delete(self.url + '/' + name, headers=api_auth)
        data = json.loads(deleted.data.decode())
        assert len(data["meta"]["deleted"]) == 1
        assert data["meta"]["deleted"][0] == created_id
