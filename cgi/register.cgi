#!/home/eaiibgrp/mmankows/perl5/perlbrew/perls/perl-5.10.0/bin/perl -I ~/perl5/lib/perl5 
use strict;
use warnings;

use lib '/home/eaiibgrp/mmankows/mtracker/lib';
use JSON::XS;
use Data::Dumper;
use CGI;
use CGI::Pretty qw/:standard/;
use DBI;
use MIME::Base64 ();

use DBTools;



my $query = CGI->new;

if( $query->request_method eq 'POST') {
    my $json;
    eval { 
        $json    = $query->param('POSTDATA');
        $json    = decode_json( $json );
        die "Wrong JSON format" if grep { not $json->{ $_ } } qw/user pass did cs/;
    };
    if ( $@ ) {
        print Dumper $json;
        print header(-type => "text/html", -status => "500");
        print "$@";
    }
} else {
        print header(-type => "text/html", -status => "404 NOT FOUND");
        print "Unsupported request type";
    
}
