@load base/frameworks/notice
@load base/files/x509

redef enum Notice::Type += { Suspicious_TLS_Cert };

event x509_certificate(f: fa_file, cert_ref: string, cert: X509::Certificate)
    {
    if ( cert$subject == cert$issuer )
        {
        print fmt("WARNING: suspicious TLS cert (self-issued) subject=%s", cert$subject);
        NOTICE([$note=Suspicious_TLS_Cert,
                $msg=fmt("Suspicious TLS cert: subject == issuer (%s)", cert$subject)]);
        }
    }
