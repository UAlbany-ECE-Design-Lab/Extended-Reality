using UnrealBuildTool;

public class X11823ClientTarget : TargetRules
{
	public X11823ClientTarget(TargetInfo Target) : base(Target)
	{
		DefaultBuildSettings = BuildSettingsVersion.V3;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		Type = TargetType.Client;
		ExtraModuleNames.Add("X11823");
	}
}
