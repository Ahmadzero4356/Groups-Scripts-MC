# Groups Scripts MC

A collection of Minecraft server scripts written in **Skript**, organized into three independent groups: server-core monitoring, GriefPrevention claim management, and administrative tools.

> **Important:** These are server-side Skript files, not a standalone plugin. Review the requirements and external command integrations in each section before deploying them. The repository includes both the extracted source folders and ZIP archives.

## Script Groups

### 1. Core Boot

![Core Boot — Minecraft server core and monitoring](Core%20boot/core-boot.jpg)

A lightweight central alert and logging layer intended to receive reports from other scripts.

**Included files**

| File | Purpose |
|---|---|
| [core_boot.sk](Core%20boot/core_boot.sk) | Maintains the core online/offline state, stores alert entries, prints INFO/WARNING/CRITICAL alerts to console, and exposes functions for status and log retrieval. |
| [event_watchdog.sk](Core%20boot/event_watchdog.sk) | Observes player movement, block breaking, chat, and command events; reports threshold activity through the Core Boot alert function. |

**Integration functions**

- `zmx_core_alert(source, level, detail, advice)` — submit a central alert.
- `zmx_core_status()` — return the core status.
- `zmx_core_log_count()` — return the number of stored core log entries.
- `zmx_core_get_logs(limit)` — retrieve recent core log entries.
- `zmx_event_get_logs(limit)` — retrieve recent Event Watchdog entries.

**Configuration highlights**

- Event Watchdog movement/chat/command warning threshold: `50`.
- Block-break warning threshold: `100`.
- Event counter reset interval: `5 seconds`.

The scripts are designed for observation and console reporting; the Core Boot file explicitly states that it does not cancel gameplay events.

### 2. Claim (GriefPrevention)

![Claim — Minecraft land protection](claim%20(GriefPrevention)/claim-griefprevention.jpg)

Connects player progression to GriefPrevention claim-block allowances, with a small player GUI and periodic claim-value checks.

**Included files**

| File | Purpose |
|---|---|
| [claim_by_level.sk](claim%20(GriefPrevention)/claim_by_level.sk) | Calculates claim-block allowance from the player's AuraSkills level, applies it on join and checks for level changes. |
| [claim_gui.sk](claim%20(GriefPrevention)/claim_gui.sk) | Provides the `/claimgui` inventory interface with level, claim-block, status, milestone, and synchronization display elements. |
| [security_guard.sk](claim%20(GriefPrevention)/security_guard.sk) | Periodically checks claim-block values and reports claim/region and low-TPS conditions to console. |

**Default claim calculation**

- Base allowance at level 1: `100` claim blocks.
- Additional allowance per level: `75` claim blocks.
- Maximum configured allowance: `50,000` claim blocks.
- Claim allowance formula: `100 + 75 × (level − 1)`, capped at the configured maximum.

The claim scripts use the console command `acb <player> set <amount>` to apply claim-block values.

**Requirements**

- Skript **2.12 or newer**.
- AuraSkills.
- GriefPrevention.
- PlaceholderAPI, with the relevant placeholders available:
  - `%auraskills_level%`
  - `%griefprevention_remainingclaims%`
- A plugin or command provider that supplies the `acb` command.

### 3. Item Admin

![Item Admin — Minecraft administrative items and tools](item%20admin/item-admin.jpg)

A rank-based administrative item and GUI concept, accompanied by audit, permission-check, quick-fix, and security-monitoring scripts.

**Included files**

| File | Purpose |
|---|---|
| [admin_item.sk](item%20admin/admin_item.sk) | Gives eligible ranks a named written book that opens the admin GUI when right-clicked. |
| [admin_gui.sk](item%20admin/admin_gui.sk) | Builds a 27-slot admin panel with rank-dependent Clan, Player, Server Monitor, Quick Commands, and Security Tools buttons. |
| [admin_permissions.sk](item%20admin/admin_permissions.sk) | Defines the `hasAdminPermission(player, action)` rank check for Owner, Admin, and Helper. |
| [admin_audit.sk](item%20admin/admin_audit.sk) | Stores admin-action entries and provides the `/auditlog` command. |
| [admin_quickfix.sk](item%20admin/admin_quickfix.sk) | Provides `/quickfix lag`, `/quickfix glitch`, and `/quickfix chunks` handlers. |
| [security_guard.sk](item%20admin/security_guard.sk) | Periodically checks player height boundaries, TPS, and loaded-plugin status, reporting findings to console. |

**Ranks represented in the scripts**

| Rank | Intended access |
|---|---|
| Owner | All defined admin actions, including Security Tools. |
| Admin | Most admin actions; Security Tools and Delete Owner Clan are excluded by the permission function. |
| Helper | Clan Management and Player Management. |

The scripts store these ranks in Skript variables under `{zmx.rank::%uuid%}`. They do not define a LuckPerms permission-node mapping in the current source.

**Commands**

| Command | Purpose |
|---|---|
| `/getadminitem` | Give the named admin book to a player whose stored rank is Owner, Admin, or Helper. |
| `/openadmingui [<player>]` | Open the administrative GUI (the current trigger operates on the executing player). |
| `/auditlog` | Display stored audit entries, subject to the script's rank-variable check. |
| `/quickfix lag` | Calls the external `lagfix` console command. |
| `/quickfix glitch` | Returns players with a stored guard alert to the world spawn and clears that alert. |
| `/quickfix chunks` | Invokes the script's chunk-regeneration loop. |

**External integrations and placeholders**

Some GUI actions deliberately call commands that must be supplied by other plugins or scripts. Examples in the current source include `openclanmenu`, `openplayermenu`, `showserverstatus`, `quickadmin`, `securitytools`, and `lagfix`. The audit script also contains example event-integration logic. These integrations should not be assumed to work until the corresponding providers and event syntax are configured and tested on the target server.

## Installation

1. Back up your server and existing Skript files.
2. Install a Minecraft server implementation supported by your chosen Skript build.
3. Install Skript. For the Claim group, use Skript 2.12 or newer.
4. Install the dependencies listed for the group you intend to use.
5. Review each script's options, placeholders, commands, and integrations.
6. Copy only the required `.sk` files into the server's `plugins/Skript/scripts/` directory, preserving a clear folder structure if desired.
7. Reload scripts from the server console or in-game with the appropriate Skript reload command.
8. Check the console for parse errors and verify each feature in a test environment before production use.

Load related scripts together where they depend on shared functions or variables. In particular, Event Watchdog calls the Core Boot alert function, and the Claim GUI and Claim Security Guard use variables established by the claim-level script.

## Repository Structure

```text
Groups-Scripts-MC/
├── Core boot/
│   ├── core_boot.sk
│   ├── event_watchdog.sk
│   └── core-boot.jpg
├── claim (GriefPrevention)/
│   ├── claim_by_level.sk
│   ├── claim_gui.sk
│   ├── security_guard.sk
│   └── claim-griefprevention.jpg
├── item admin/
│   ├── admin_audit.sk
│   ├── admin_gui.sk
│   ├── admin_item.sk
│   ├── admin_permissions.sk
│   ├── admin_quickfix.sk
│   ├── security_guard.sk
│   └── item-admin.jpg
├── Core boot.zip
├── claim (GriefPrevention).zip
├── item admin.zip
└── README.md
```

## Compatibility and Deployment Notes

- Only the Claim group explicitly specifies a minimum Skript version in its source header. Confirm compatibility of the other scripts with your server, Skript version, and installed addons.
- PlaceholderAPI placeholders must be available and return usable values; verify the relevant expansions before enabling the Claim group.
- Commands referenced from scripts must exist on the server. Replace or implement integration placeholders where necessary.
- Test GUI click handling, rank assignment, console commands, and recovery actions on a staging server first.
- These files are provided as scripts for server administrators. No claim is made that every optional integration is preconfigured for every server environment.

## License

No license file is currently included. Unless a license is added, all rights remain with the repository owner; contact the owner before redistributing or incorporating the scripts into another project.
