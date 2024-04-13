using UnrealBuildTool;

public class X11823EditorTarget : TargetRules
{
	public X11823EditorTarget(TargetInfo Target) : base(Target)
	{
		DefaultBuildSettings = BuildSettingsVersion.V3;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		Type = TargetType.Editor;
		ExtraModuleNames.Add("X11823");
	}
}
