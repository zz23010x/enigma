

local _M = {}

_M.GRAVITY                   =   0.0012  --重力
_M.LEADER_JUMP_SPEED         =   0.62    --跳跃初始速度
_M.STIR_UP_AGAIN_SPEED       =   0.24    --2次挑起速度
_M.HIT_DOWN_SPEED            =   0.8     --击倒向下的速度
_M.HIT_BODY_STOP_TIME        =   30      --攻击打到人停顿时间
_M.EFFECT_HIT_BODY_STOP_TIME =   30      --特效打到人停顿时间
_M.NORMAL_SPX_SPEED          =   100     --一般人物spx的播放速度
_M.SHUIJING_SPX_SPEED        =   150     --水晶spx的播放速度
_M.STUN_SPX_SPEED            =   100     --眩晕特效播放速度
_M.TOUCH_EFFECT_SPX_SPEED    =   40      --触摸特效播放速度
_M.NORMAL_ROLE_GET_UP_TIMES  =   300     --怪物起身无敌时间
_M.ROLE_RESAFE_GET_UP_TIMES  =   1000    --人物起身无敌时间
_M.ROLE_BOSS_RESAFE_TIMES    =   10000   --世界boss复活无敌时间
_M.STIR_UP_RATIO_SML         =   0.3     --普通倒地弹起系数
_M.STIR_UP_RATIO_BIG         =   0.9     --boss倒地弹起系数
_M.STIR_UP_AGAIN_SPEED_MAX   =   0.3     --2次挑起的最大速度
_M.STIR_UP_AGAIN_RATIO       =   0.5     --超过2次挑起最大速度时乘以的系数
_M.SPRINT_JUMP_MOVE_SPEED    =   0.65    --冲刺跳起的移动速度
_M.SPRINT_FAREST             =   40000   --冲刺最大距离
_M.SPRINT_SHORTEST           =   170     --冲刺最短距离
_M.SPRINT_SPEED              =   0.6     --冲刺速度
_M.SPRINT_PRIORITY           =   4       --冲刺优先级
_M.STUN_TIME                 =   2500    --眩晕时间
_M.DEBUFF_ICE_TIME           =   2000    --冰冻时间
_M.DEBUFF_RAIN_TIME          =   500     --酸雨时间
_M.DEBUFF_BLOOD_TIME         =   100     --吸血时间
_M.COMMON_DEAD_STIRUPSPEED   =   0.15    --普通怪物死亡后飞起的速度y
_M.COMMON_DEAD_STIRXSPEED    =   0.03    --普通怪物死亡后飞出的速度x
_M.SPECIAL_DEAD_STIRUPSPEED  =   0.5     --特殊怪物（boss、精英）死亡后飞起的速度y
_M.SPECIAL_DEAD_STIRXSPEED   =   0.1     --特殊怪物（boss、精英）死亡后飞出的速度x
_M.DEBUFF_POISON_TIME        =   20000   --中毒时间
_M.DEBUFF_POISON_HURT_GAP    =   2000    --中毒隔多长时间产生一次伤害

_M.teachOpen                 =   true    --是否开启教学

return _M

