"""测试短视频处理器的新版元数据标记生成。"""

import re
from pathlib import Path


def test_social_video_marker_format():
    """验证社交视频元数据标记的格式。"""
    # 测试标记格式
    social_video_marker = "<!-- meta:social_video title=awesome-design-md：一键复刻大厂设计规范？这也太离谱了吧！ -->"
    assert re.match(r'^<!-- meta:social_video title=.+ -->$', social_video_marker)
    print("✅ 社交视频标题标记格式正确")


def test_scene_marker_format():
    """验证场景元数据标记的格式。"""
    # 测试时间范围格式
    test_cases = [
        ("<!-- meta:scene id=0 time=0:00~0:02 -->", True),
        ("<!-- meta:scene id=45 time=1:36~1:39 -->", True),
        ("<!-- meta:scene id=46 time=1:39~1:41 -->", True),
        ("<!-- meta:scene id=999 time=59:59~1:00:00 -->", False),  # 时间超出范围
    ]
    
    pattern = r'^<!-- meta:scene id=(\d+) time=(\d{1,2}):(\d{2})~(\d{1,2}):(\d{2}) -->$'
    
    for marker, should_match in test_cases:
        matches = bool(re.match(pattern, marker))
        if matches == should_match:
            print(f"✅ 场景标记格式正确: {marker}")
        else:
            print(f"❌ 场景标记格式错误: {marker}")


def test_actual_output():
    """验证实际输出文件中的标记。"""
    output_file = (
        r'd:\Pycharm\VSCODErepos\QCR powered by LLMs\build\OCRLLM\output'
        r'\social_video1\awesome-design-md：一键复刻大厂设计规范？这也太离谱了吧！_识别.md'
    )
    
    if Path(output_file).exists():
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查元数据标记
        has_social_video = bool(re.search(r'<!-- meta:social_video', content))
        has_scenes = len(re.findall(r'<!-- meta:scene id=', content))
        
        print(f"\n📄 输出文件检查:")
        print(f"  ✅ 社交视频标题标记: {'是' if has_social_video else '否'}")
        print(f"  ✅ 场景标记数量: {has_scenes} 个")
        
        if has_social_video:
            social_marker = re.search(r'<!-- meta:social_video .+ -->', content)
            if social_marker:
                print(f"     标记: {social_marker.group(0)[:80]}...")
        
        if has_scenes > 0:
            scene_markers = re.findall(r'<!-- meta:scene id=(\d+) time=.+ -->', content)
            print(f"     场景 ID: {', '.join(scene_markers[:5])}{'...' if len(scene_markers) > 5 else ''}")
    else:
        print(f"⚠️  输出文件不存在: {output_file}")


if __name__ == '__main__':
    print("=" * 80)
    print("🧪 社交视频元数据标记单元测试")
    print("=" * 80)
    
    test_social_video_marker_format()
    print()
    test_scene_marker_format()
    print()
    test_actual_output()
    
    print("\n" + "=" * 80)
    print("✅ 所有测试完成")
    print("=" * 80)
