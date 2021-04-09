from colorfulpanda.utils.main import Printer, Formator
from colorfulpanda.Style.Red import style0, style1, style2, style3
import time

ONE_F = '''
       c                 ]                            -
         $              Q$    in    $@              $
          ${            $?    W$     $`           .$
           $,          $W     $$     u$           $i
            $         x(      $$|     'p         $,
            [$         $      $$      $         $p
        $<   x$j      *'$     $$o    $:$      }$B   ^$
          $   Y$$$$   ?@$$   $$$ L  $$8Y   $$$$$   $+
            $$w   @@$$ $$$  $$~$$$  M$$`o$$&}  -$$
             '$$   #$$ $Z$$$ &$$@ $$$t$ $$@   $$O
              $$$  $$$$j$ .-  t$$   >$"$$$$  $$$1
               $$$i $$$$$ $$$ $$ $$$Bh$$$$' $$$l
                $$$  $$$$$ {$$$$$$z $$$$$  $$$
                '$$|  $$$$$$.$$$$ $$$$$$} '$$|
        ".       $  $$$.  :$$C|f $$[   $$$  8        l
           $(        ;$$$$boB    fMm$$$$&        >$
              $        :  C$ $$$$}$b  +        $x
              ( \C  d@ &$$ou$$$$$$dC$$$.#&  ;x <.
                !$?$$$$$$$$$$ +{ $$$$$$$$$$)$?
             $n    $$$l   $$j$$$$%$$~  `$$$.   :$
                         mJ$      $o .
                          $lt    B1$;
                          $$m&_+$ $$
                         ;$$'     $$$
                        $            $
'''

SEC_F = '''
      .                 ...    L    :$"           L$
       .@;.             ${    $$    . xl.        &@
         Z$            $B     $$ .   X@`.       $*
         ']$          $ '    j$$~   m$i<    ./B$^   $$
            $o '      .@   . ^$$$$  $@$.-$$$m . C$k
       .$m . $$$@ .   $o$...<$$$}l$@$]C\$$k.'+$B'.
           r$$.  @b$$ Q$$I. $L$$.)$$$,$@$@B.a$$$
            :W$$!  $$$ "$$$$]$$$$$!.$$$$$.'$$$
             .$$$..$$$$$.$@$.1$$ $$$0wkf i*$@l
               $$$n h@$@$$'*@$$$uQ  :$$@$  .      \$
        .       $$?$$[. .Z$$]C$$$iY . w     . {$ '
        . 8o      . .$$$$@r$t  @$.$@$$$$$!v$ n?  .
            ..$"     }@ .?:!$$$$$C$@ . t$$$'.  ?$.
               $]$qn$$$$@$$@v$$  '$.$.
         . '@!   '{$$ . .J$$$$$m'$$c
'''

def main():
	p = Printer()
	f = Formator()
	f.screen.clear_screen()
	pic1 = p.multi_in_style(SEC_F, style0, f)
	p.pln(pic1)
	time.sleep(0.1)
	f.screen.clear_screen()
	pic1 = p.multi_in_style(ONE_F, style1, f)
	p.pln(pic1)
	time.sleep(0.1)
	f.screen.clear_screen()
	pic2 = p.multi_in_style(ONE_F, style2, f)
	p.pln(pic2)
	time.sleep(0.1)
	f.screen.clear_screen()
	pic3 = p.multi_in_style(ONE_F, style3, f)
	p.pln(pic3)