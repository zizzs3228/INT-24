rule R1
{
    meta:
        description = "Capturing Executable Files"
    strings:
        $bin_bash = "/bin/bash"
        $bin_sh = "/bin/sh"
    condition:
        any of ($bin_bash, $bin_sh)
}

rule R2
{
    meta:
        description = "Capturing file manipulation commands"
    strings:
        $scp = "scp"
        $cat = "cat"
        $binary = "binary"
        $chmod = "chmod"
    condition:
        any of ($scp, $cat, $binary, $chmod)
}

rule R3
{
    meta:
        description = "Capturing Commands for Obtaining Sensitive Information"
    strings:
        $whoami = "whoami"
        $hostname = "hostname"
        $pwd = "pwd"
    condition:
        any of ($whoami, $hostname, $pwd)
}

rule R4
{
    meta:
        description = "Capturing Networking Commands"
    strings:
        $wget = "wget"
        $curl = "curl"
        $nc = "nc"
        $nslookup = "nslookup"
    condition:
        any of ($wget, $curl, $nc, $nslookup)
}

rule R5
{
    meta:
        description = "Capturing sensitive commands"
    strings:
        $base64 = "base64"
        $b64 = "b64"
    condition:
        any of ($base64, $b64)
}

rule R6
{
    meta:
        description = "Capturing Sensitive Files or Folders"
    strings:
        $etc_rc = "etc/rc"
        $etc_passwd = "etc/passwd"
        $profile = "/.profile"
    condition:
        any of ($etc_rc, $etc_passwd, $profile)
}

rule R7
{
    meta:
        description = "Capturing commands that execute .exe file"
    strings:
        $exe_files = /.*\.exe/
    condition:
        $exe_files
}

rule R8
{
    meta:
        description = "Capturing Suspicious Files"
    strings:
        $sh_files = /\.sh/
        $exec_files = /\.exec/
    condition:
        any of ($sh_files, $exec_files)
}