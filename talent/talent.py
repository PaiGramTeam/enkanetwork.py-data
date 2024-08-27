import json
from typing import Any, Dict, Optional, List, Tuple
from pathlib import Path

CHARACTER_MAP: Dict[str, Dict[str, Any]] = {}
SKILLS_MAP: Dict[str, Dict[str, Any]] = {}
TALENTS_MAP: Dict[str, List[Dict[str, int]]] = {}  # 角色简称为键
FINAL_TALENTS_MAP: Dict[str, Dict[str, Dict[str, int]]] = {}  # 角色 ID 为键

exports_path = Path("exports") / "data"
characters_path = exports_path / "characters.json"
skills_path = exports_path / "skills.json"
talents_save_path = exports_path / "talents.json"
talents_path = Path("temp")


def get_character_key(icon_name: str, ele: str) -> Optional[str]:
    if not icon_name:
        return None
    if not icon_name.startswith("UI_AvatarIcon_"):
        print(f"异常 icon_name {icon_name}")
        return None
    name = icon_name.replace("UI_AvatarIcon_", "")
    if "Player" in name:
        return f"{name}_{ele}"
    return name


def load_characters() -> None:
    global CHARACTER_MAP
    CHARACTER_MAP.clear()
    with open(characters_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for k, v in data.items():
            v["id"] = k
            if len(v.get("skills", [])) < 3:
                continue
            key = get_character_key(v.get("iconName", ""), v.get("costElemType", ""))
            if not key:
                continue
            CHARACTER_MAP[key] = v


def load_skills() -> None:
    global SKILLS_MAP
    SKILLS_MAP.clear()
    with open(skills_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        SKILLS_MAP.update(data)


def get_talent_key(file_name: Path) -> Tuple[str, str]:
    name = file_name.name.replace("ConfigTalent_", "").replace(".json", "")
    if "Player" in name:
        return name.replace("Player", "PlayerBoy"), name.replace("Player", "PlayerGirl")
    return name, ""


def get_constellation(key: str, cons: List[int], con_map: Dict[str, int]) -> int:
    if "S_Levelup" in key or "E_Levelup" in key:
        if not con_map:
            if len(cons) >= 4:
                con_map.update({"S_Levelup": 5, "E_Levelup": 3})
            else:
                con_map.update({"S_Levelup": 3, "E_Levelup": 5})
        for k, v in con_map.items():
            if k in key:
                return v
    return int(key.split("_")[-1]) % 10


def parse_talent_config(data: Dict[str, Any]) -> List[Dict[str, int]]:
    values = []
    keys = list(data.keys())
    need_talent = not any(["Constellation" in key for key in keys])
    cons = []
    con_map = {}
    for k, v in data.items():
        if need_talent and "Talent" not in k:
            continue
        if not need_talent and "Constellation" not in k:
            continue
        try:
            constellation = get_constellation(k, cons, con_map)
            cons.append(constellation)
        except:
            print(f"错误的命座名称: {k}")
            continue
        for v1 in v:
            _data = {
                "constellation": constellation,
                "talent_type": v1.get("talentType"),
                "talent_index": v1.get("talentIndex"),
                "extra_level": v1.get("extraLevel"),
            }
            if not all(_data.values()):
                continue
            values.append(_data)
    return values


def load_talent_configs() -> None:
    global TALENTS_MAP
    TALENTS_MAP.clear()
    for file_name in talents_path.glob("*.json"):
        key1, key2 = get_talent_key(file_name)
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
            values = parse_talent_config(data)
            TALENTS_MAP[key1] = values
            if key2:
                TALENTS_MAP[key2] = values


def fix_talent_configs() -> None:
    global TALENTS_MAP, FINAL_TALENTS_MAP
    FINAL_TALENTS_MAP.clear()
    for k, v in TALENTS_MAP.items():
        ch = CHARACTER_MAP.get(k)
        if not ch:
            print(f"错误的角色简称 {k}")
            continue
        ch_id = ch["id"]
        ch_skills = ch["skills"]
        skill_map = {1: None, 2: None, 9: None}
        for skill in ch_skills:
            skill_data = SKILLS_MAP[str(skill)]
            proud_skill_group_id = skill_data["proudSkillGroupId"]
            if not proud_skill_group_id:
                continue
            skill_key = proud_skill_group_id % 10
            skill_map[skill_key] = proud_skill_group_id
        new_data = {}
        for v1 in v:
            talent_index = v1["talent_index"]
            v1["proud_skill_group_id"] = skill_map[talent_index]
            new_data[str(v1["constellation"])] = v1
        FINAL_TALENTS_MAP[ch_id] = new_data


def save_talent_configs() -> None:
    sorted_dict = dict(sorted(FINAL_TALENTS_MAP.items()))
    with open(talents_save_path, "w", encoding="utf-8") as f:
        json.dump(sorted_dict, f, ensure_ascii=False, indent=4)


def main():
    load_characters()
    load_skills()
    load_talent_configs()
    fix_talent_configs()
    save_talent_configs()
