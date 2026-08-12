#!/usr/bin/env python3
"""Run a bounded Firefox/Marionette smoke check against a loopback GUI host."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse


DEFAULT_URL = "http://127.0.0.1:7878/"
DEFAULT_PORT = 2828
LOOPBACK_HOSTS = {"127.0.0.1", "::1"}
EXPECTED_PAGE_TITLE = "Vital Margin — Executive Desktop"
EXPECTED_COMPETITIVE_TURNS = 24
EXPECTED_CAMPAIGN_STAGE_COUNTS = {
  "stabilization-v1": 5,
  "regional-affiliation-v1": 6,
}
CAMPAIGN_LABELS = {
  "competitive-regional-v1": "competitive regional",
  "stabilization-v1": "stabilization",
  "regional-affiliation-v1": "regional affiliation",
}
FIREFOX_CANDIDATES = (
  "/Applications/Firefox.app/Contents/MacOS/firefox",
  "/usr/bin/firefox",
  "/usr/local/bin/firefox",
)


def _packet_bytes(payload: object) -> bytes:
  data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
  return str(len(data)).encode("ascii") + b":" + data


class MarionetteClient:
  def __init__(self, host: str, port: int, timeout: float = 15.0):
    self.socket = socket.create_connection((host, port), timeout=timeout)
    self.socket.settimeout(timeout)
    self.message_id = 0

  def close(self) -> None:
    self.socket.close()

  def _receive(self) -> object:
    header = bytearray()
    while b":" not in header:
      part = self.socket.recv(1)
      if not part:
        raise RuntimeError("Firefox Marionette closed before sending a packet")
      header.extend(part)
    length = int(header[:-1])
    data = bytearray()
    while len(data) < length:
      part = self.socket.recv(length - len(data))
      if not part:
        raise RuntimeError("Firefox Marionette closed during a packet")
      data.extend(part)
    return json.loads(data.decode("utf-8"))

  def command(self, name: str, parameters: dict) -> object:
    self.message_id += 1
    self.socket.sendall(_packet_bytes([0, self.message_id, name, parameters]))
    response = self._receive()
    if not isinstance(response, list) or len(response) < 4:
      raise RuntimeError(f"unexpected Marionette response: {response!r}")
    if response[0] != 1 or response[1] != self.message_id:
      raise RuntimeError(f"unexpected Marionette response ID: {response!r}")
    if response[2] is not None:
      raise RuntimeError(response[2])
    return response[3]


def _find_firefox(explicit: str | None) -> str:
  candidates = [explicit] if explicit else []
  candidates.extend(FIREFOX_CANDIDATES)
  for candidate in candidates:
    if candidate and Path(candidate).is_file():
      return candidate
  discovered = shutil.which("firefox")
  if discovered:
    return discovered
  raise RuntimeError("Firefox executable not found")


def _validate_loopback_url(url: str) -> None:
  parsed = urlparse(url)
  if parsed.scheme not in {"http", "https"} or parsed.hostname not in LOOPBACK_HOSTS:
    raise RuntimeError("runtime smoke URL must use an HTTP(S) loopback host")
  if parsed.username or parsed.password:
    raise RuntimeError("runtime smoke URL must not include credentials")


def validate_observations(
  shell: object,
  host: object,
  url: str,
  browser: object,
  marionette_protocol: object,
  resume: object | None = None,
  campaign_launches: object | None = None,
  competitive_full_campaign: object | None = None,
  campaign_full_runs: object | None = None,
) -> None:
  if not isinstance(shell, dict) or not isinstance(host, dict) or not isinstance(browser, dict):
    raise RuntimeError("Firefox runtime smoke observations must be objects")
  runtime_errors = []
  if marionette_protocol != 3:
    runtime_errors.append("Firefox Marionette protocol is not version 3")
  if browser.get("name") != "firefox":
    runtime_errors.append("browser identity is not Firefox")
  if not isinstance(browser.get("version"), str) or not browser["version"].strip():
    runtime_errors.append("Firefox browser version is missing")
  if not isinstance(browser.get("platform"), str) or not browser["platform"].strip():
    runtime_errors.append("Firefox platform capability is missing")
  if browser.get("headless") is not True:
    runtime_errors.append("Firefox headless capability is missing")
  if runtime_errors:
    raise RuntimeError("; ".join(runtime_errors))
  shell_errors = []
  if shell.get("title") != EXPECTED_PAGE_TITLE:
    shell_errors.append("page title does not match the executive desktop shell")
  if shell.get("url") != url:
    shell_errors.append("shell URL does not match the requested loopback URL")
  if shell.get("ready") != "complete":
    shell_errors.append("document did not reach readyState=complete")
  if shell.get("start_control") is not True:
    shell_errors.append("session-start control is missing")
  if shell.get("demo_fixture") is not True:
    shell_errors.append("demo fixture was not present before host start")
  if shell_errors:
    raise RuntimeError("; ".join(shell_errors))

  host_errors = []
  status = host.get("status")
  if not isinstance(status, str) or not status.startswith("competitive regional session loaded: "):
    host_errors.append("host did not report a competitive regional session load")
  session = host.get("session")
  if not isinstance(session, str) or not re.fullmatch(r"session-[A-Za-z0-9_-]+", session):
    host_errors.append("host did not return a non-empty opaque session ID")
  if host.get("demo_fixture") is not False:
    host_errors.append("demo fixture remained present after host start")
  if host.get("checkpoint_saved") is not True:
    host_errors.append("host checkpoint save did not report success")
  if not isinstance(host.get("checkpoint_status"), str) or not host["checkpoint_status"].startswith("Host checkpoint saved at "):
    host_errors.append("host checkpoint save status is missing")
  if host_errors:
    raise RuntimeError("; ".join(host_errors))
  if resume is not None:
    if not isinstance(resume, dict):
      raise RuntimeError("Firefox resume observation must be an object")
    session = host.get("session")
    resume_errors = []
    if resume.get("status") != f"Host session refreshed after browser refresh: {session}":
      resume_errors.append("browser refresh did not report the expected host refresh")
    if resume.get("session") != session:
      resume_errors.append("browser refresh changed the opaque session ID")
    if resume.get("stored_session_id") != session:
      resume_errors.append("browser refresh storage did not retain only the opaque session ID")
    if resume.get("demo_fixture") is not False:
      resume_errors.append("demo fixture remained present after browser refresh resume")
    if resume.get("ready") != "complete":
      resume_errors.append("browser refresh resume did not reach readyState=complete")
    if resume_errors:
      raise RuntimeError("; ".join(resume_errors))
  if campaign_launches is not None:
    if not isinstance(campaign_launches, dict):
      raise RuntimeError("Firefox campaign launch observations must be an object")
    campaign_errors = []
    campaign_sessions = []
    for campaign, label in CAMPAIGN_LABELS.items():
      observation = campaign_launches.get(campaign)
      if not isinstance(observation, dict):
        campaign_errors.append(f"missing Firefox campaign launch observation: {campaign}")
        continue
      expected_status = f"{label} session loaded: {observation.get('session')}"
      if observation.get("status") != expected_status:
        campaign_errors.append(f"unexpected Firefox campaign launch status: {campaign}")
      if not isinstance(observation.get("session"), str) or not re.fullmatch(
        r"session-[A-Za-z0-9_-]+", observation["session"]
      ):
        campaign_errors.append(f"invalid opaque Firefox campaign session ID: {campaign}")
      else:
        campaign_sessions.append(observation["session"])
      if observation.get("demo_fixture") is not False:
        campaign_errors.append(f"demo fixture remained after Firefox campaign launch: {campaign}")
      if observation.get("ready") != "complete":
        campaign_errors.append(f"Firefox campaign launch did not reach readyState=complete: {campaign}")
    competitive_launch = campaign_launches.get("competitive-regional-v1")
    if isinstance(competitive_launch, dict) and competitive_launch.get("session") != host.get("session"):
      campaign_errors.append("competitive campaign launch changed the host session ID")
    if len(campaign_sessions) == len(CAMPAIGN_LABELS) and len(set(campaign_sessions)) != len(campaign_sessions):
      campaign_errors.append("Firefox campaign launches reused an opaque session ID")
    if campaign_errors:
      raise RuntimeError("; ".join(campaign_errors))
  if competitive_full_campaign is not None:
    if not isinstance(competitive_full_campaign, dict):
      raise RuntimeError("Firefox competitive full-campaign observation must be an object")
    full_campaign_errors = []
    if competitive_full_campaign.get("campaign") != "competitive-regional-v1":
      full_campaign_errors.append("full-campaign observation is not competitive regional")
    if competitive_full_campaign.get("session") != host.get("session"):
      full_campaign_errors.append("full-campaign observation changed the host session ID")
    if competitive_full_campaign.get("target_turns") != EXPECTED_COMPETITIVE_TURNS:
      full_campaign_errors.append("full-campaign target turn count is not 24")
    if competitive_full_campaign.get("committed_turns") != EXPECTED_COMPETITIVE_TURNS:
      full_campaign_errors.append("full-campaign committed turn count is not 24")
    if competitive_full_campaign.get("history_count") != EXPECTED_COMPETITIVE_TURNS:
      full_campaign_errors.append("full-campaign history count is not 24")
    if competitive_full_campaign.get("replay_count") != EXPECTED_COMPETITIVE_TURNS:
      full_campaign_errors.append("full-campaign replay count is not 24")
    if competitive_full_campaign.get("autosave_count") != EXPECTED_COMPETITIVE_TURNS:
      full_campaign_errors.append("full-campaign autosave count is not 24")
    turns = competitive_full_campaign.get("turns")
    if not isinstance(turns, list) or len(turns) != EXPECTED_COMPETITIVE_TURNS:
      full_campaign_errors.append("full-campaign turn observations are incomplete")
    else:
      for expected_turn, observation in enumerate(turns, start=1):
        if not isinstance(observation, dict):
          full_campaign_errors.append(f"full-campaign turn {expected_turn} is not an object")
          continue
        if observation.get("turn") != expected_turn:
          full_campaign_errors.append(f"full-campaign turn ordering is invalid at {expected_turn}")
        if observation.get("command") != "hold":
          full_campaign_errors.append(f"full-campaign command is not Hold at {expected_turn}")
        if observation.get("history_count") != expected_turn:
          full_campaign_errors.append(f"full-campaign history count is invalid at {expected_turn}")
        if observation.get("replay_count") != expected_turn:
          full_campaign_errors.append(f"full-campaign replay count is invalid at {expected_turn}")
        autosave_status = observation.get("autosave_status")
        expected_autosave = f"Host autosave completed at {expected_turn} committed transitions."
        if autosave_status != expected_autosave:
          full_campaign_errors.append(f"full-campaign autosave status is invalid at {expected_turn}")
        state_hash = observation.get("state_hash")
        if not isinstance(state_hash, str) or not re.fullmatch(r"[0-9a-f]+", state_hash):
          full_campaign_errors.append(f"full-campaign state hash is invalid at {expected_turn}")
    terminal = competitive_full_campaign.get("terminal")
    if not isinstance(terminal, dict):
      full_campaign_errors.append("full-campaign terminal observation is missing")
    else:
      if terminal.get("status") != "Host session ended; final history and debrief loaded":
        full_campaign_errors.append("full-campaign terminal status is invalid")
      if terminal.get("history_count") != EXPECTED_COMPETITIVE_TURNS:
        full_campaign_errors.append("full-campaign terminal history count is not 24")
      if not isinstance(terminal.get("debrief_count"), int) or terminal["debrief_count"] <= 0:
        full_campaign_errors.append("full-campaign terminal debrief is missing")
      if not isinstance(terminal.get("final_state_hash"), str) or not re.fullmatch(
        r"[0-9a-f]+", terminal["final_state_hash"]
      ):
        full_campaign_errors.append("full-campaign terminal state hash is invalid")
    if full_campaign_errors:
      raise RuntimeError("; ".join(full_campaign_errors))
  if campaign_full_runs is not None:
    if not isinstance(campaign_full_runs, dict):
      raise RuntimeError("Firefox campaign full-transition observations must be an object")
    coverage_errors = []
    for campaign, target_stages in EXPECTED_CAMPAIGN_STAGE_COUNTS.items():
      observation = campaign_full_runs.get(campaign)
      launch = campaign_launches.get(campaign) if isinstance(campaign_launches, dict) else None
      if not isinstance(observation, dict):
        coverage_errors.append(f"missing Firefox full-transition observation: {campaign}")
        continue
      if not isinstance(launch, dict) or observation.get("session") != launch.get("session"):
        coverage_errors.append(f"full-transition observation changed the host session ID: {campaign}")
      if observation.get("campaign") != campaign:
        coverage_errors.append(f"full-transition observation has the wrong campaign: {campaign}")
      if observation.get("target_stages") != target_stages:
        coverage_errors.append(f"full-transition target stage count is invalid: {campaign}")
      if observation.get("committed_stages") != target_stages:
        coverage_errors.append(f"full-transition committed stage count is invalid: {campaign}")
      if observation.get("history_count") != target_stages:
        coverage_errors.append(f"full-transition history count is invalid: {campaign}")
      if observation.get("autosave_count") != target_stages:
        coverage_errors.append(f"full-transition autosave count is invalid: {campaign}")
      stages = observation.get("stages")
      if not isinstance(stages, list) or len(stages) != target_stages:
        coverage_errors.append(f"full-transition stage observations are incomplete: {campaign}")
      else:
        for expected_stage, stage in enumerate(stages, start=1):
          if not isinstance(stage, dict):
            coverage_errors.append(f"full-transition stage is not an object: {campaign} {expected_stage}")
            continue
          if stage.get("stage") != expected_stage:
            coverage_errors.append(f"full-transition stage ordering is invalid: {campaign} {expected_stage}")
          if stage.get("history_count") != expected_stage:
            coverage_errors.append(f"full-transition stage history count is invalid: {campaign} {expected_stage}")
          if stage.get("autosave_status") != f"Host autosave completed at {expected_stage} committed transitions.":
            coverage_errors.append(f"full-transition autosave status is invalid: {campaign} {expected_stage}")
          if not isinstance(stage.get("state_hash"), str) or not re.fullmatch(r"[0-9a-f]+", stage["state_hash"]):
            coverage_errors.append(f"full-transition state hash is invalid: {campaign} {expected_stage}")
      terminal = observation.get("terminal")
      if not isinstance(terminal, dict):
        coverage_errors.append(f"full-transition terminal observation is missing: {campaign}")
      else:
        if terminal.get("status") != "Host session ended; final history and debrief loaded":
          coverage_errors.append(f"full-transition terminal status is invalid: {campaign}")
        if terminal.get("history_count") != target_stages:
          coverage_errors.append(f"full-transition terminal history count is invalid: {campaign}")
        if not isinstance(terminal.get("debrief_count"), int) or terminal["debrief_count"] <= 0:
          coverage_errors.append(f"full-transition terminal debrief is missing: {campaign}")
        if not isinstance(terminal.get("final_state_hash"), str) or not re.fullmatch(
          r"[0-9a-f]+", terminal["final_state_hash"]
        ):
          coverage_errors.append(f"full-transition terminal state hash is invalid: {campaign}")
    if coverage_errors:
      raise RuntimeError("; ".join(coverage_errors))


def _wait_for_port(host: str, port: int, timeout: float) -> None:
  deadline = time.monotonic() + timeout
  while time.monotonic() < deadline:
    try:
      with socket.create_connection((host, port), timeout=0.5):
        return
    except OSError:
      time.sleep(0.1)
  raise RuntimeError(f"Firefox Marionette did not open {host}:{port}")


def _execute(client: MarionetteClient, session_id: str, script: str) -> object:
  result = client.command(
    "WebDriver:ExecuteScript",
    {"sessionId": session_id, "script": script, "args": []},
  )
  return result.get("value") if isinstance(result, dict) else result


def _wait_for(
  client: MarionetteClient,
  session_id: str,
  script: str,
  predicate: object,
  description: str,
  timeout: float = 5.0,
) -> object:
  deadline = time.monotonic() + timeout
  latest = None
  while time.monotonic() < deadline:
    latest = _execute(client, session_id, script)
    if callable(predicate) and predicate(latest):
      return latest
    time.sleep(0.05)
  raise RuntimeError(f"Firefox runtime smoke timed out waiting for {description}: {latest!r}")


def _run_competitive_full_campaign(
  client: MarionetteClient,
  session_id: str,
  host_session_id: str,
) -> dict:
  turns = []
  for turn in range(1, EXPECTED_COMPETITIVE_TURNS + 1):
    _execute(client, session_id, """
      const button = document.querySelector('form[data-action-id="hold"] button[type="submit"]');
      if (!button) throw new Error('competitive Hold action form is unavailable');
      button.click();
      return true;
    """)
    _wait_for(
      client,
      session_id,
      "return {draft_count: document.querySelectorAll('#draft-action-list > li').length};",
      lambda value: isinstance(value, dict) and value.get("draft_count") == 1,
      f"Hold draft for turn {turn}",
    )
    _execute(client, session_id, "document.querySelector('#validate-actions').click(); return true;")
    _wait_for(
      client,
      session_id,
      "return {valid: document.querySelector('#submit-month')?.hidden === false, text: document.querySelector('#validation-status')?.textContent || ''};",
      lambda value: isinstance(value, dict)
      and value.get("valid") is True
      and str(value.get("text", "")).startswith("Plan checked:"),
      f"host validation for turn {turn}",
    )
    _execute(client, session_id, "document.querySelector('#submit-month').click(); return true;")
    snapshot = _wait_for(
      client,
      session_id,
      """
        const replay = document.querySelector('#replay-playback-status')?.textContent || '';
        const replayMatch = replay.match(/ of (\\d+)/);
        const hashes = [...document.querySelectorAll('#history-list .hash')];
        return {
          history_count: document.querySelectorAll('#history-list > li').length,
          replay_count: replayMatch ? Number(replayMatch[1]) : 0,
          autosave_status: document.querySelector('#session-launch-status')?.textContent || '',
          state_hash_text: hashes.length ? hashes[hashes.length - 1].textContent : ''
        };
      """,
      lambda value: isinstance(value, dict)
      and value.get("history_count") == turn
      and value.get("replay_count") == turn
      and value.get("autosave_status") == f"Host autosave completed at {turn} committed transitions.",
      f"host commit, replay, and autosave for turn {turn}",
      timeout=8.0,
    )
    state_hash_match = re.search(r"state hash: ([0-9a-f]+)", str(snapshot.get("state_hash_text", "")))
    turns.append({
      "turn": turn,
      "command": "hold",
      "history_count": snapshot.get("history_count"),
      "replay_count": snapshot.get("replay_count"),
      "autosave_status": snapshot.get("autosave_status"),
      "state_hash": state_hash_match.group(1) if state_hash_match else "",
    })
  _execute(client, session_id, "document.querySelector('#session-end').click(); return true;")
  terminal = _wait_for(
    client,
    session_id,
    "return {status: document.querySelector('#session-status')?.textContent || '', history_count: document.querySelectorAll('#history-list > li').length, debrief_count: document.querySelectorAll('#debrief-list > li').length, meta: document.querySelector('#session-meta')?.textContent || ''};",
    lambda value: isinstance(value, dict)
    and value.get("status") == "Host session ended; final history and debrief loaded"
    and value.get("history_count") == EXPECTED_COMPETITIVE_TURNS
    and isinstance(value.get("debrief_count"), int)
    and value.get("debrief_count") > 0,
    "host terminal history and debrief",
  )
  final_hash_match = re.search(r"hash ([0-9a-f]+)", str(terminal.get("meta", "")))
  return {
    "campaign": "competitive-regional-v1",
    "session": host_session_id,
    "target_turns": EXPECTED_COMPETITIVE_TURNS,
    "committed_turns": len(turns),
    "history_count": terminal.get("history_count"),
    "replay_count": EXPECTED_COMPETITIVE_TURNS,
    "autosave_count": len(turns),
    "turns": turns,
    "terminal": {
      "status": terminal.get("status"),
      "history_count": terminal.get("history_count"),
      "debrief_count": terminal.get("debrief_count"),
      "final_state_hash": final_hash_match.group(1) if final_hash_match else "",
    },
  }


def _best_effort_end_current_host_session(client: MarionetteClient, session_id: str) -> bool:
  try:
    state = _execute(client, session_id, """
      return {
        session: document.querySelector('#session-id')?.value || '',
        end_available: Boolean(document.querySelector('#session-end') && !document.querySelector('#session-end').disabled)
      };
    """)
    if not isinstance(state, dict) or not state.get("session") or not state.get("end_available"):
      return False
    _execute(client, session_id, "document.querySelector('#session-end').click(); return true;")
    _wait_for(
      client,
      session_id,
      "return document.querySelector('#session-status')?.textContent || '';",
      lambda value: value == "Host session ended; final history and debrief loaded",
      "best-effort host session cleanup",
      timeout=5.0,
    )
    return True
  except Exception:
    return False


def _run_campaign_coverage(
  client: MarionetteClient,
  session_id: str,
  host_session_id: str,
  campaign: str,
) -> dict:
  target_stages = EXPECTED_CAMPAIGN_STAGE_COUNTS[campaign]
  stages = []
  for stage in range(1, target_stages + 1):
    _execute(client, session_id, """
      const form = document.querySelector('#action-preview-list form');
      if (!form) throw new Error('campaign action form is unavailable');
      for (const field of form.querySelectorAll('input, select')) {
        if (field.tagName === 'SELECT') field.value = field.options[0]?.value || '';
        else field.value = field.min || '0';
      }
      const submit = form.querySelector('button[type="submit"]');
      if (!submit) throw new Error('campaign coverage submit control is unavailable');
      submit.click();
      return true;
    """)
    snapshot = _wait_for(
      client,
      session_id,
      """
        const history = [...document.querySelectorAll('#campaign-history-list > li')]
          .filter((item) => !item.classList.contains('empty'));
        return {
          history_count: history.length,
          autosave_status: document.querySelector('#session-launch-status')?.textContent || '',
          state_hash_text: history.length ? history[history.length - 1].textContent : ''
        };
      """,
      lambda value: isinstance(value, dict)
      and value.get("history_count") == stage
      and value.get("autosave_status") == f"Host autosave completed at {stage} committed transitions.",
      f"host commit and autosave for {campaign} stage {stage}",
      timeout=8.0,
    )
    state_hash_match = re.search(r"state hash: ([0-9a-f]+)", str(snapshot.get("state_hash_text", "")))
    stages.append({
      "stage": stage,
      "history_count": snapshot.get("history_count"),
      "autosave_status": snapshot.get("autosave_status"),
      "state_hash": state_hash_match.group(1) if state_hash_match else "",
    })
  _execute(client, session_id, "document.querySelector('#session-end').click(); return true;")
  terminal = _wait_for(
    client,
    session_id,
    "return {status: document.querySelector('#session-status')?.textContent || '', history_count: document.querySelectorAll('#history-list > li').length, debrief_count: document.querySelectorAll('#debrief-list > li').length, meta: document.querySelector('#session-meta')?.textContent || ''};",
    lambda value: isinstance(value, dict)
    and value.get("status") == "Host session ended; final history and debrief loaded"
    and value.get("history_count") == target_stages
    and isinstance(value.get("debrief_count"), int)
    and value.get("debrief_count") > 0,
    f"host terminal {campaign} history and debrief",
  )
  final_hash_match = re.search(r"hash ([0-9a-f]+)", str(terminal.get("meta", "")))
  return {
    "campaign": campaign,
    "session": host_session_id,
    "target_stages": target_stages,
    "committed_stages": len(stages),
    "history_count": terminal.get("history_count"),
    "autosave_count": len(stages),
    "stages": stages,
    "terminal": {
      "status": terminal.get("status"),
      "history_count": terminal.get("history_count"),
      "debrief_count": terminal.get("debrief_count"),
      "final_state_hash": final_hash_match.group(1) if final_hash_match else "",
    },
  }


def _start_campaign(client: MarionetteClient, session_id: str, campaign: str) -> object:
  script = f"""
    const select = document.querySelector('#session-campaign');
    select.value = {json.dumps(campaign)};
    select.dispatchEvent(new Event('change', {{bubbles: true}}));
    document.querySelector('#session-start').click();
    return true;
  """
  _execute(client, session_id, script)
  time.sleep(1.0)
  return _execute(client, session_id, """
    return {
      status: document.querySelector('#session-launch-status')?.textContent || '',
      session: document.querySelector('#session-id')?.value || '',
      demo_fixture: document.body.innerText.includes('Demo fixture loaded'),
      ready: document.readyState
    };
  """)


def run_probe(url: str = DEFAULT_URL, firefox_bin: str | None = None) -> dict:
  _validate_loopback_url(url)
  firefox = _find_firefox(firefox_bin)
  with tempfile.TemporaryDirectory(prefix="hs-firefox-runtime-") as profile:
    process = subprocess.Popen(
      [
        firefox,
        "--headless",
        "--new-instance",
        "--profile",
        profile,
        "--marionette",
        "--remote-allow-hosts",
        "127.0.0.1",
        url,
      ],
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      text=True,
    )
    client = None
    session_id = None
    try:
      _wait_for_port("127.0.0.1", DEFAULT_PORT, 15.0)
      client = MarionetteClient("127.0.0.1", DEFAULT_PORT)
      hello = client._receive()
      created = client.command(
        "WebDriver:NewSession",
        {"capabilities": {"alwaysMatch": {"browserName": "firefox"}, "firstMatch": []}},
      )
      session_id = created["sessionId"]
      capabilities = created["capabilities"]
      client.command("WebDriver:Navigate", {"sessionId": session_id, "url": url})
      time.sleep(0.5)
      shell = _execute(client, session_id, """
        return {
          title: document.title,
          ready: document.readyState,
          start_control: Boolean(document.querySelector('#session-start')),
          demo_fixture: document.body.innerText.includes('Demo fixture loaded'),
          url: location.href
        };
      """)
      _execute(client, session_id, "document.querySelector('#session-start').click(); return true;")
      time.sleep(1.0)
      host = _execute(client, session_id, """
        return {
          status: document.querySelector('#session-launch-status')?.textContent || '',
          session: document.querySelector('#session-id')?.value || '',
          demo_fixture: document.body.innerText.includes('Demo fixture loaded'),
          campaign: 'competitive-regional-v1',
          ready: document.readyState
        };
      """)
      _execute(client, session_id, "document.querySelector('#session-save').click(); return true;")
      time.sleep(0.5)
      checkpoint_status = _execute(
        client,
        session_id,
        "return document.querySelector('#session-launch-status')?.textContent || '';",
      )
      checkpoint_saved = (
        isinstance(checkpoint_status, str)
        and checkpoint_status.startswith("Host checkpoint saved at ")
      )
      if not checkpoint_saved:
        raise RuntimeError("explicit host checkpoint save did not report success")
      stored_session_id = _execute(
        client,
        session_id,
        "return localStorage.getItem('hs-mgt-active-session-id');",
      )
      client.command("WebDriver:Refresh", {"sessionId": session_id})
      time.sleep(1.0)
      resume = _execute(client, session_id, """
        return {
          status: document.querySelector('#session-launch-status')?.textContent || '',
          session: document.querySelector('#session-id')?.value || '',
          stored_session_id: localStorage.getItem('hs-mgt-active-session-id'),
          demo_fixture: document.body.innerText.includes('Demo fixture loaded'),
          ready: document.readyState
        };
      """)
      competitive_full_campaign = _run_competitive_full_campaign(client, session_id, host["session"])
      host["checkpoint_saved"] = checkpoint_saved
      host["checkpoint_status"] = checkpoint_status
      host["stored_session_id"] = stored_session_id
      browser = {
        "name": capabilities.get("browserName"),
        "version": capabilities.get("browserVersion"),
        "platform": capabilities.get("platformName"),
        "headless": capabilities.get("moz:headless"),
      }
      stabilization_launch = _start_campaign(client, session_id, "stabilization-v1")
      stabilization_full = _run_campaign_coverage(
        client, session_id, stabilization_launch["session"], "stabilization-v1"
      )
      affiliation_launch = _start_campaign(client, session_id, "regional-affiliation-v1")
      affiliation_full = _run_campaign_coverage(
        client, session_id, affiliation_launch["session"], "regional-affiliation-v1"
      )
      campaign_launches = {
        "competitive-regional-v1": host,
        "stabilization-v1": stabilization_launch,
        "regional-affiliation-v1": affiliation_launch,
      }
      campaign_full_runs = {
        "stabilization-v1": stabilization_full,
        "regional-affiliation-v1": affiliation_full,
      }
      validate_observations(
        shell,
        host,
        url,
        browser,
        hello.get("marionetteProtocol"),
        resume,
        campaign_launches,
        competitive_full_campaign,
        campaign_full_runs,
      )
      client.command("WebDriver:DeleteSession", {"sessionId": session_id})
      session_id = None
      return {
        "status": "pass",
        "url": url,
        "marionette_protocol": hello.get("marionetteProtocol"),
        "browser": browser,
        "shell": shell,
        "host_start": host,
        "browser_refresh_resume": resume,
        "campaign_launches": campaign_launches,
        "competitive_full_campaign": competitive_full_campaign,
        "campaign_full_runs": campaign_full_runs,
      }
    finally:
      if client is not None:
        if session_id is not None:
          _best_effort_end_current_host_session(client, session_id)
          try:
            client.command("WebDriver:DeleteSession", {"sessionId": session_id})
          except (OSError, RuntimeError):
            pass
        client.close()
      if process.poll() is None:
        process.terminate()
        try:
          process.wait(timeout=5)
        except subprocess.TimeoutExpired:
          process.kill()
          process.wait(timeout=5)


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", default=DEFAULT_URL)
  parser.add_argument("--firefox-bin")
  args = parser.parse_args()
  try:
    print(json.dumps(run_probe(args.url, args.firefox_bin), indent=2, sort_keys=True))
  except (OSError, RuntimeError, TimeoutError, KeyError, TypeError) as error:
    print(json.dumps({"status": "fail", "errors": [str(error)]}, indent=2, sort_keys=True))
    return 1
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
