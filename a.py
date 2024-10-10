PRG0404 START ; 教科書 PRG0307
    LAD     GR1,10
    LAD     GR2,10
    LAD     GR3,10
    LAD     GR4,100
    LAD     GR5,100
    LAD     GR6,100
    SLA     GR1,1 ; 10×2
    SLA     GR2,2 ; 10×4
    SLA     GR3,3 ; 10×8
    SRA     GR4,1 ; 100÷2
    SRA     GR5,2 ; 100÷4
    SRA     GR6,3 ; 100÷8
    RET
    END