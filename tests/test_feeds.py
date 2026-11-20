import os

from vscan_controller.models.feeds import Feeds


def test_port_list_parsing_xml_to_model():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "feeds.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    response = Feeds.from_xml(xml_content)

    # --- Booleans ---
    assert response.feed_owner_set is True
    assert response.feed_roles_set is True
    assert response.feed_resources_access is True

    # --- Feed Count ---
    assert len(response.feeds) == 4

    # --- Feed 1: NVT ---
    nvt = response.feeds[0]
    assert nvt.type == "NVT"
    assert nvt.name == "Greenbone Community Feed"
    assert nvt.version == "202608100823"
    assert "Greenbone Community Feed" in nvt.description
    assert "https://www.greenbone.net/en/feed-comparison/" in nvt.description
    assert nvt.sync_not_available is None
    assert nvt.currently_syncing is None

    # --- Feed 2: SCAP ---
    scap = response.feeds[1]
    assert scap.type == "SCAP"
    assert scap.name == "Greenbone SCAP Data Feed"
    assert scap.version == "202608100626"
    assert scap.description == "Provided via feed-automation"
    assert scap.sync_not_available is None
    assert scap.currently_syncing is None

    # --- Feed 3: CERT ---
    cert = response.feeds[2]
    assert cert.type == "CERT"
    assert cert.name == "Greenbone CERT Data Feed"
    assert cert.version == "202608100444"
    assert cert.description == "Provided via feed-automation as container image"
    assert cert.sync_not_available is None
    assert cert.currently_syncing is None

    # --- Feed 4: GVMD_DATA ---
    gvmd = response.feeds[3]
    assert gvmd.type == "GVMD_DATA"
    assert gvmd.name == "Greenbone Data Objects Feed"
    assert gvmd.version == "202608100532"
    assert gvmd.description == "Provided via feed-automation"
    assert gvmd.sync_not_available is None
    assert gvmd.currently_syncing is None
