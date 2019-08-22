for %%i in (D:\new\Lua\lua_encrypt\luaPreEncrypt\*.lua) do (
luac -o "D:\new\Lua\lua_encrypt\luaEncrypt\%%~nxi" %%i 
)

pause