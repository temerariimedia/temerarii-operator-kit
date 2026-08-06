import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// ANGLE is the reliable GL backend on Windows; leave it unless a render fails to start.
Config.setChromiumOpenGlRenderer("angle");
