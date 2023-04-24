try:
  import os
  import time
  import json
  import logging
  import datetime
  import requests
  import coloredlogs
except ImportError as e:
  print(f'{e.name} module is not installed. Please run "packages.bat" to install the necessary modules before running the program.')
  time.sleep(5)
  exit()

os.system('cls')
os.system('TITLE V-Bucks Alerts Bot by Liqutch')
coloredlogs.logging.basicConfig(level=coloredlogs.logging.INFO)
log = coloredlogs.logging.getLogger(__name__)
coloredlogs.install(fmt="[%(asctime)s][%(levelname)s] %(message)s", datefmt="%H:%M:%S", logger=log)

if not os.path.isfile('settings.json') or not os.path.isfile('localization.json'):       
  log.error('Configuration files not found, program is closing...')
  time.sleep(5)
  exit()

try:
  with open("settings.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    lastcheck = data["last_check"]
    checkrate = data["checkrate"]
    title = data["title"]
    lang = data["language"]
    webhook = data["webhook_url"]
    account_id = data["account_id"]
    device_id = data["device_id"]
    secret = data["secret"]
except:
  log.error("There was a problem retrieving the configuration settings. Please ensure that the file is properly configured.")
  time.sleep(5)
  exit()

try:
  with open("localization.json", "r", encoding="utf-8") as f:
    localization = json.load(f)
except:
  log.error("There was a problem retrieving the language settings. Please ensure that the file is properly configured.")
  time.sleep(5)
  exit()
try:
  now = datetime.datetime.now()
  reflesh = False
  def refleshToken():
    url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    body = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"
    headers = {
      "Authorization":
      "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=",
      "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=body, headers=headers)
    if response.status_code == 400:
      if reflesh == False:
        log.error("Token could not be created. Please check your informations.")
      elif reflesh == True:
        log.error("Token could not be refreshed. Please check your informations.")
      time.sleep(5)
      exit()
    if response.status_code == 200:
      if reflesh == False:
        log.info("Token successfully created.")
      elif reflesh == True:
        log.info("Token successfully refreshed.")
      return response.json()["access_token"]
  token = refleshToken()
  reflesh = True
  tokentime = now
  while True:
    with open("settings.json") as f:
      data = json.load(f)
      lastcheck = data["last_check"]
      checkrate = data["checkrate"]
    now = datetime.datetime.now()
    if (now - tokentime).total_seconds() >= 3600:
      token = refleshToken()
    base_url = "https://fortnitecentral.genxgames.gg/api/v1/export?path="
    all_theaters = "/Game/Balance/DataTables/GameDifficultyGrowthBounds.GameDifficultyGrowthBounds"
    utc_now = (datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z').split("T")[0]
    worldinfo = requests.get("https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/world/info", headers={"Authorization": f"Bearer {token}"})
    nextRefresh = worldinfo.json()["missionAlerts"][0]["nextRefresh"].split("T")[0]
    if lastcheck != nextRefresh and utc_now != lastcheck.split("T")[0]:
      log.info("Mission alerts updated!")
      data = worldinfo.json()
      fields = []
      vbucks = 0
      count = 0
      try:
        for i, mission_alert in enumerate(data.get("missionAlerts", [])):
          for available_alert in mission_alert.get("availableMissionAlerts", []):
            for reward in available_alert.get("missionAlertRewards", {}).get("items", []):
              if reward.get("itemType") == "AccountResource:currency_mtxswap":
                tile_index = available_alert.get("tileIndex")
                quantity = reward.get("quantity")
                zoneTheme = data["theaters"][i]["tiles"][tile_index]["zoneTheme"]
                files = requests.get(base_url + zoneTheme.split(".")[0])
                key = files.json()["jsonOutput"][1]["Properties"]["ZoneName"]["key"]
                try:
                  mission = localization["zoneNames"][key][lang]
                except:
                  mission = localization["zoneNames"][key]["en"]
                  log.error("Language not found while retrieving task details. Automatically selecting => English.")
                missions = data.get("missions", [])[i]
                for available_mission in missions.get("availableMissions", []):
                  if available_mission.get("tileIndex") == tile_index:
                    theater = available_mission.get("missionDifficultyInfo", {}).get("rowName")
                    missionGenerator = available_mission.get("missionGenerator")
                    def missionNames(missionGenerator):
                      if "_1Gate_" in missionGenerator or "_Cat1FtS_" in missionGenerator:
                        return localization["missions"]["029003B949368614A8DABBA356C1C2BB"][lang]
                      if "_2Gates_" in missionGenerator:
                        return localization["missions"]["6D79CF67497338EB3C220A98DE3B6188"][lang]
                      if "_3Gates_" in missionGenerator:
                        return localization["missions"]["CAFB5B6E4D10DE114B3A4A8180DFD2DC"][lang]
                      if "_4Gates_" in missionGenerator:
                        return localization["missions"]["EFFBDC1A4D6701DD500C0BADCFA4AB97"][lang]
                      if "_DtB_" in missionGenerator:
                        return localization["missions"]["35C0CEF64FFC9CE340D0579D68B53E0F"][lang]
                      if "_EtShelter_" in missionGenerator:
                        return localization["missions"]["F553B25F4E64D39E17709EB887016B1E"][lang]
                      if "_RtD_" in missionGenerator or "_RetrieveTheData_" in missionGenerator:
                        return localization["missions"]["136A7B9041D6CF2AADA4CE9D7EB942FB"][lang]
                      if "_LtB_" in missionGenerator or "_RideTheLightning_" in missionGenerator or "_LaunchTheBalloon_" in missionGenerator or "_RtL_" in missionGenerator:
                        return localization["missions"]["96F9DB85441C355E089DB28B382ADECA"][lang]
                      if "_RtS_" in missionGenerator:
                        return localization["missions"]["FCDA9A38436EB6427D5B248DC98AF055"][lang]
                    missionName = missionNames(missionGenerator)
                    theaters = requests.get(base_url + all_theaters)
                    power = theaters.json()["jsonOutput"][0]["Rows"][theater]["ThreatDisplayName"]["sourceString"]
                    area = localization["theaters"][i - 1][lang]
                    fields.append({
                      "name": f"<:vbucks:1089610011258400960> {quantity} - {missionName} [{power}]",
                      "value": f"{area} - {mission}"
                    })
                    vbucks += int(quantity)
                    count += 1
      except:
        log.error("There was an error while retrieving mission details. Please try again later or seek support.")
      if count == 0:
        embed_data = {
          "title": title,
          "description": "There are no V-Bucks mission alerts today.",
          "color": 39423
        }
      else:
        embed_data = {
          "title": title,
          "color": 39423,
          "fields": fields,
          "footer": {
            "text": "Total: " + str(vbucks) + " V-Bucks"
          }
        }
      post_data = {
        "content": None,
        "embeds": [embed_data],
        "attachments": []
      }
      try:
        with open("settings.json", "r+") as f:
          data = json.load(f)
          data["last_check"] = datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
          f.seek(0)
          json.dump(data, f, indent=2, ensure_ascii=False)
      except:
        log.error("There was a problem retrieving the configuration settings. Please ensure that the file is properly configured.")
        time.sleep(5)
        exit()
      else:
        post = requests.post(webhook, data=json.dumps(post_data), headers={"Content-Type": "application/json"})
        if post.status_code == 204:
          log.info("Webhook successfully sent.")
        else:
          log.error("There was an error while sending the webhook.")
          time.sleep(5)
          exit()
    else:
      log.info("Waiting for new mission alerts.")
    time.sleep(checkrate)
except:
  log.error("An unknown error occurred. Please try again later or seek support.")