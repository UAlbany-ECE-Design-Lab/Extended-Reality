using UnrealBuildTool;

public class X11823ServerTarget : TargetRules
{
	public X11823ServerTarget(TargetInfo Target) : base(Target)
	{
		DefaultBuildSettings = BuildSettingsVersion.V3;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		Type = TargetType.Server;
		ExtraModuleNames.Add("X11823");
	}
}
