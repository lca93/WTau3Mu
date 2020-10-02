for file in "$@"; do
 ln -s $PWD/$file $CMSSW_BASE/bin/$SCRAM_ARCH
 chmod +xwr $PWD/$file
done
