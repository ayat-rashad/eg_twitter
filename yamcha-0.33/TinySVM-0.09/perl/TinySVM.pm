# This file was automatically generated by SWIG
package TinySVM;
require Exporter;
require DynaLoader;
@ISA = qw(Exporter DynaLoader);
package TinySVMc;
bootstrap TinySVM;
var_TinySVM_init();
package TinySVM;
@EXPORT = qw( );

# ---------- BASE METHODS -------------

package TinySVM;

sub TIEHASH {
    my ($classname,$obj) = @_;
    return bless $obj, $classname;
}

sub CLEAR { }

sub FIRSTKEY { }

sub NEXTKEY { }

sub this {
    my $ptr = shift;
    return tied(%$ptr);
}


# ------- FUNCTION WRAPPERS --------

package TinySVM;


############# Class : TinySVM::BaseExample ##############

package TinySVM::BaseExample;
@ISA = qw( TinySVM );
%OWNER = ();
%ITERATORS = ();
*add = *TinySVMc::BaseExample_add;
*set = *TinySVMc::BaseExample_set;
*get = *TinySVMc::BaseExample_get;
*remove = *TinySVMc::BaseExample_remove;
*clear = *TinySVMc::BaseExample_clear;
*size = *TinySVMc::BaseExample_size;
*read = *TinySVMc::BaseExample_read;
*write = *TinySVMc::BaseExample_write;
*readSVindex = *TinySVMc::BaseExample_readSVindex;
*writeSVindex = *TinySVMc::BaseExample_writeSVindex;
sub DESTROY {
    return unless $_[0]->isa('HASH');
    my $self = tied(%{$_[0]});
    delete $ITERATORS{$self};
    if (exists $OWNER{$self}) {
        TinySVMc::delete_BaseExample($self);
        delete $OWNER{$self};
    }
}

*append = *TinySVMc::BaseExample_append;
*appendSVindex = *TinySVMc::BaseExample_appendSVindex;
*getDimension = *TinySVMc::BaseExample_getDimension;
*getNonzeroDimension = *TinySVMc::BaseExample_getNonzeroDimension;
*getY = *TinySVMc::BaseExample_getY;
*getX = *TinySVMc::BaseExample_getX;
*getAlpha = *TinySVMc::BaseExample_getAlpha;
*getGradient = *TinySVMc::BaseExample_getGradient;
*getG = *TinySVMc::BaseExample_getG;
sub DISOWN {
    my $self = shift;
    my $ptr = tied(%$self);
    delete $OWNER{$ptr};
    };

sub ACQUIRE {
    my $self = shift;
    my $ptr = tied(%$self);
    $OWNER{$ptr} = 1;
    };


############# Class : TinySVM::Model ##############

package TinySVM::Model;
@ISA = qw( TinySVM TinySVM::BaseExample );
%OWNER = ();
%ITERATORS = ();
*read = *TinySVMc::Model_read;
*write = *TinySVMc::Model_write;
*clear = *TinySVMc::Model_clear;
*classify = *TinySVMc::Model_classify;
*estimateMargin = *TinySVMc::Model_estimateMargin;
*estimateSphere = *TinySVMc::Model_estimateSphere;
*estimateVC = *TinySVMc::Model_estimateVC;
*estimateXA = *TinySVMc::Model_estimateXA;
*compress = *TinySVMc::Model_compress;
*getSVnum = *TinySVMc::Model_getSVnum;
*getBSVnum = *TinySVMc::Model_getBSVnum;
*getTrainingDataSize = *TinySVMc::Model_getTrainingDataSize;
*getLoss = *TinySVMc::Model_getLoss;
sub new {
    my $self = shift;
    my @args = @_;
    $self = TinySVMc::new_Model(@args);
    return undef if (!defined($self));
    bless $self, "TinySVM::Model";
    $OWNER{$self} = 1;
    my %retval;
    tie %retval, "TinySVM::Model", $self;
    return bless \%retval,"TinySVM::Model";
}

sub DESTROY {
    return unless $_[0]->isa('HASH');
    my $self = tied(%{$_[0]});
    delete $ITERATORS{$self};
    if (exists $OWNER{$self}) {
        TinySVMc::delete_Model($self);
        delete $OWNER{$self};
    }
}

sub DISOWN {
    my $self = shift;
    my $ptr = tied(%$self);
    delete $OWNER{$ptr};
    };

sub ACQUIRE {
    my $self = shift;
    my $ptr = tied(%$self);
    $OWNER{$ptr} = 1;
    };


############# Class : TinySVM::Example ##############

package TinySVM::Example;
@ISA = qw( TinySVM TinySVM::BaseExample );
%OWNER = ();
%ITERATORS = ();
*read = *TinySVMc::Example_read;
*write = *TinySVMc::Example_write;
*rebuildSVindex = *TinySVMc::Example_rebuildSVindex;
sub learn {
    my @args = @_;
    my $result = TinySVMc::Example_learn(@args);
    return undef if (!defined($result));
    my %resulthash;
    tie %resulthash, ref($result), $result;
    return bless \%resulthash, ref($result);
}
sub new {
    my $self = shift;
    my @args = @_;
    $self = TinySVMc::new_Example(@args);
    return undef if (!defined($self));
    bless $self, "TinySVM::Example";
    $OWNER{$self} = 1;
    my %retval;
    tie %retval, "TinySVM::Example", $self;
    return bless \%retval,"TinySVM::Example";
}

sub DESTROY {
    return unless $_[0]->isa('HASH');
    my $self = tied(%{$_[0]});
    delete $ITERATORS{$self};
    if (exists $OWNER{$self}) {
        TinySVMc::delete_Example($self);
        delete $OWNER{$self};
    }
}

sub DISOWN {
    my $self = shift;
    my $ptr = tied(%$self);
    delete $OWNER{$ptr};
    };

sub ACQUIRE {
    my $self = shift;
    my $ptr = tied(%$self);
    $OWNER{$ptr} = 1;
    };


# ------- VARIABLE STUBS --------

package TinySVM;

1;
