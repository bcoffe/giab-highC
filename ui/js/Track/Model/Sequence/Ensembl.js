Genoverse.Track.Model.Sequence.Ensembl = Genoverse.Track.Model.Sequence.extend({
  url              : '//rest.ensembl.org/sequence/region/human/__CHR__:__START__-__END__?content-type=text/plain;coord_system_version=GRCh37', // Example url*/
  dataRequestLimit : 10000000 // As per e! REST API restrictions
});
