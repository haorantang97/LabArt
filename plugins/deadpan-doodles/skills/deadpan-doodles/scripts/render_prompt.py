#!/usr/bin/env python3
"""Assemble a local Sha Bing image-call bundle. No network or image generation."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MODES = {"generate", "edit", "correct-material", "correct-shape", "correct-line"}
TYPES = {"portrait", "animal", "plant", "object", "scene"}
COMMON = {"mode", "anchor", "reference_mode", "exception_reason"}
GENERATE = {"subject_type", "subject", "scene", "identity", "allocation",
            "construction", "bleed", "aspect", "text", "subject_references"}
EDIT = {"target", "change"}
STYLE_DRIFT = re.compile(
    r"(?:蜡笔|油画|矢量)(?:风格|画风|质感)|3D渲染|三维渲染|赛博朋克风|统一色板|固定色板|"
    r"粗黑描边|全图做旧|高光大眼|专业绘本风|"
    r"\b(?:crayon style|oil painting style|vector art style|photorealistic|cyberpunk style)\b",
    re.I,
)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def nonempty(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} 必须是非空文本")
    return value

def content(value, name):
    value = nonempty(value, name)
    if "【" in value or "{{" in value or "}}" in value:
        raise ValueError(f"{name} 含疑似未填占位符；请写具体内容")
    if STYLE_DRIFT.search(value):
        raise ValueError(f"{name} 混入另一套画风；请移出内容字段并单独声明实验")
    return value

def regular_file(value, base, name):
    value = nonempty(value, name)
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base / path
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"{name} 文件不存在：{path}")
    return path

def locked_file(root, record):
    path = (root / record["path"]).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("配方/资产路径越出 skill 目录")
    if not path.is_file():
        raise ValueError(f"固定文件缺失：{path}")
    data = path.read_bytes()
    if sha(data) != record["sha256"]:
        raise ValueError(f"固定文件校验不符：{path.name}；请核验版本，不可自动接受")
    return path, data

def recipe_section(source, name):
    fence = chr(96) * 3
    pattern = r"^## " + re.escape(name) + r"\n\n" + fence + r"text\n(.*?)\n" + fence
    matches = re.findall(pattern, source, re.M | re.S)
    if len(matches) != 1:
        raise ValueError(f"配方区块缺失或重复：{name}")
    return matches[0]

def reference(path, role, instruction):
    return {"path": str(path), "role": role, "instruction": instruction,
            "sha256": sha(path.read_bytes())}

def build(request, base, root=ROOT):
    if not isinstance(request, dict):
        raise ValueError("请求必须是 JSON 对象")
    mode = request.get("mode")
    if mode not in MODES:
        raise ValueError("mode 必须明确为 generate、edit 或三种 correct-* 模式")
    allowed = COMMON | (GENERATE if mode == "generate" else EDIT)
    unknown = set(request) - allowed
    if unknown:
        raise ValueError("不支持的字段：" + ", ".join(sorted(unknown)))
    reference_mode = request.get("reference_mode", "standard")
    if reference_mode not in {"standard", "none"}:
        raise ValueError("reference_mode 必须为 standard 或 none")
    if reference_mode == "none":
        nonempty(request.get("exception_reason"), "exception_reason")
    elif "exception_reason" in request:
        raise ValueError("标准模式不需要 exception_reason")
    manifest = json.loads((root / "assets/manifest.json").read_text(encoding="utf-8"))
    _, recipe_data = locked_file(root, manifest["recipe"])
    source = recipe_data.decode("utf-8")
    anchor_name = request.get("anchor", "canonical")
    if anchor_name not in manifest["anchors"]:
        raise ValueError("未知风格参考：" + str(anchor_name))
    refs = []
    parts = []
    if mode != "generate":
        target = regular_file(request.get("target"), base, "target")
        refs.append(reference(target, "edit-target", "用户选定的编辑目标；保留未点名部分。"))
    if reference_mode == "standard":
        anchor_path, _ = locked_file(root, manifest["anchors"][anchor_name])
        role = ("画法、气质和抽象形状分配参考；跨题材不复制其中人物或动物的身份、"
                "器官、发型、眼镜、衣服、配色与构图。用户明确沿用其主体形状时同时保留形状关系。")
        refs.append(reference(anchor_path, "style-anchor", role))
    if mode == "generate":
        subject_type = request.get("subject_type")
        if subject_type not in TYPES:
            raise ValueError("subject_type 必须为 portrait、animal、plant、object 或 scene")
        subject = content(request.get("subject"), "subject")
        allocation = request.get("allocation")
        if not isinstance(allocation, dict) or set(allocation) != {"dominant", "cluster", "support"}:
            raise ValueError("allocation 必须且只含 dominant、cluster、support")
        for key, value in allocation.items():
            content(value, "allocation." + key)
        construction = content(request.get("construction"), "construction")
        bleed = content(request.get("bleed"), "bleed")
        for key in ("scene", "identity"):
            if key in request:
                content(request[key], key)
        extra_refs = request.get("subject_references", [])
        if not isinstance(extra_refs, list):
            raise ValueError("subject_references 必须为数组")
        roles = {
            "identity": "仅提供本次主体辨识，不用正常解剖或摄影光影覆盖选定的形状关系。",
            "selected-shape": "用户选定的主体形状与疏密关系；不要用其他参考把它修正常。",
        }
        for item in extra_refs:
            if not isinstance(item, dict) or set(item) != {"path", "role"}:
                raise ValueError("主体参考必须且只含 path 与 role")
            if item["role"] not in roles:
                raise ValueError("主体参考 role 必须为 identity 或 selected-shape")
            path = regular_file(item["path"], base, "subject_reference")
            refs.append(reference(path, item["role"], roles[item["role"]]))
        parts.append(recipe_section(source, "core"))
        if subject_type == "portrait":
            parts.append(recipe_section(source, "portrait"))
        body = [
            "本次内容：", "主体：" + subject,
            "形状分配—主块：" + allocation["dominant"],
            "形状分配—细节簇：" + allocation["cluster"],
            "形状分配—连接或支撑：" + allocation["support"],
            "生涩构造位置：" + construction, "水色外洇位置：" + bleed,
        ]
        for key, label in (("scene", "场景与故事"), ("identity", "辨识特征")):
            if key in request:
                body.append(label + "：" + request[key])
        if "aspect" in request:
            aspect = nonempty(request["aspect"], "aspect")
            if not re.fullmatch(r"[1-9]\d*:[1-9]\d*", aspect):
                raise ValueError("aspect 使用正整数宽:高，例如 3:4")
            body.append("画幅宽高比：" + aspect)
        if "text" in request:
            body.append("画面文字原文（只呈现引号内内容）：" +
                        json.dumps(nonempty(request["text"], "text"), ensure_ascii=False))
        else:
            body.append("不加文字、签名、Logo 或水印。")
        parts.append("\n".join(body))
    else:
        parts.append(recipe_section(source, mode))
        parts.append("本次点名修改：" + content(request.get("change"), "change"))
    for index, ref in enumerate(refs, 1):
        ref["image_index"] = index
    reference_header = ["输入图角色（与实际附图顺序一致）："]
    reference_header.extend(f"Image {r['image_index']}: {r['instruction']}" for r in refs)
    if reference_mode == "none":
        reference_header.append("本次按用户明确要求不带风格图；属于实验调用，不声称与标准附图等效。")
    prompt = "\n\n".join(["\n".join(reference_header)] + parts)
    return {
        "revision": manifest["revision"],
        "status": "standard-bundle" if reference_mode == "standard" else "experimental-no-style-anchor",
        "aesthetic_status": "not-assessed",
        "prompt": prompt, "prompt_sha256": sha(prompt.encode("utf-8")),
        "recipe_sha256": sha(recipe_data), "request": request, "references": refs,
        "referenced_image_paths": [r["path"] for r in refs],
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        request_path = args.request.expanduser().resolve()
        request = json.loads(request_path.read_text(encoding="utf-8"))
        output = json.dumps(build(request, request_path.parent), ensure_ascii=False, indent=2) + "\n"
        if args.out:
            # Never overwrite a previous call record or a source request.
            with args.out.expanduser().open("x", encoding="utf-8") as handle:
                handle.write(output)
            print(str(args.out.expanduser().resolve()))
        else:
            print(output, end="")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("组装失败：" + str(exc), file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
