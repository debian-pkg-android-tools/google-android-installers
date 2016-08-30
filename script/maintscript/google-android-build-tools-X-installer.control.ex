
Package: google-android-build-tools-$X-installer
Multi-Arch: foreign
Architecture: i386 amd64
Depends: zlib1g,
         libstdc++6,
         ${googleAndroidInstallers:Depends},
         ${misc:Depends},
Description: Google build tools $X for Android (aapt, aidl, dexdump, dx)
 This package will download the binary Google Android build tools and create a
 Debian package.  The build tools are used in the process of assembling the
 java code into the APK package.  They can also be useful for inspecting APKs.
 .
 WARNING: Installing this Debian package causes $Y to
 be downloaded from dl.google.com and/or from other suggested mirrors. The End
 User License Agreement of this binary package is available at
 developer.android.com.
