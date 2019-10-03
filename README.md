# Mail Recon

The purpose of this tool is to perform some recon against a provided domain to discover 
where it may be possible to deliver their mail. For example, users of proofpoint in the US typically have 
MX records of mx1-us1.ppe-hosted.com and mx2-us1.ppe-hosted.com or something similar.

However, it may be possible through DNS records to discover where mail is actually hosted, 
and bypass these spam protections by delivering direct to the provider. Usually, email security services
instruct organizations to whitelist the service provider's mail servers for inbound mail, denying incoming 
mail from all other sources. Often times, organizations may fail to configure this properly. That's where this 
tool comes in.

This is a work in progress, so please contact me or submit a PR for any enhancements. Thanks