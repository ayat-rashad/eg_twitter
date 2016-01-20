# Generated automatically from Makefile.PL.in by configure.
use ExtUtils::MakeMaker;
# See lib/ExtUtils/MakeMaker.pm for details of how to influence
# the contents of the Makefile that is written.
WriteMakefile(
    'CC'		=> 'c++',
    'NAME'		=> 'TinySVM',
    'INC'		=> '-I/usr/local/include',
    'LIBS'        	=> '-L/usr/local/lib -ltinysvm',
    'OBJECT'            => 'TinySVM_wrap.o'
);
