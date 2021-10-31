<%@ Application Language="C#" %>
<%@import namespace="Microsoft.IdentityModel.Web"%>
<%@import namespace="Microsoft.IdentityModel.Tokens"%>
<%@import namespace="Microsoft.IdentityModel.Web.Configuration"%>
<%@import namespace="System.Collections.Generic"%>

<script runat="server">

    void Application_Start(object sender, EventArgs e) 
    {
        // Code that runs on application startup
        FederatedAuthentication.ServiceConfigurationCreated += OnServiceConfigurationCreated;
    }
    
    
    private void OnServiceConfigurationCreated(object sender, ServiceConfigurationCreatedEventArgs e)
    {
        List<CookieTransform> sessionTransforms =
            new List<CookieTransform>(
                new CookieTransform[] 
            {
                new DeflateCookieTransform(), 
                new RsaEncryptionCookieTransform(
                    e.ServiceConfiguration.ServiceCertificate),
                new RsaSignatureCookieTransform(
                    e.ServiceConfiguration.ServiceCertificate)  
            });
        SessionSecurityTokenHandler sessionHandler =
         new SessionSecurityTokenHandler(sessionTransforms.AsReadOnly());

        e.ServiceConfiguration.SecurityTokenHandlers.AddOrReplace(sessionHandler);           

    }

    
    void Application_End(object sender, EventArgs e) 
    {
        //  Code that runs on application shutdown
    }

        
    void Application_Error(object sender, EventArgs e) 
    { 
        // Code that runs when an unhandled error occurs
        Exception ex = Context.Error;
        if(ex.Message.StartsWith("ID3206:"))
        {    
            if (!(Request.ApplicationPath.EndsWith("/")))
            {
                Response.Redirect(Request.Path + "/");
            }
        }
        else if (ex.Message.StartsWith("ID1014:") || ex.Message.StartsWith("Unexpected end of file."))
        {
            //corrupted SSO cookie
            //We flush these cookies, so the user needs to log in again instead of throwing an error
            FlushSSOCookies();
        }
    }


    void Session_Start(object sender, EventArgs e) 
    {
        // Code that runs when a new session is started

    }


    void Session_End(object sender, EventArgs e) 
    {
        // Code that runs when a session ends. 
        // Note: The Session_End event is raised only when the sessionstate mode
        // is set to InProc in the Web.config file. If session mode is set to StateServer 
        // or SQLServer, the event is not raised.

    }

    
    void FlushSSOCookies()
    {
        int limit = Request.Cookies.Count;
        for (int i=0; i<limit; i++)
        {
            String cookieName = Request.Cookies[i].Name;
            if (cookieName.StartsWith("FedAuth") || cookieName.StartsWith("ASP.NET_SessionId"))
            {    
                HttpCookie aCookie = new HttpCookie(cookieName);
                aCookie.Expires = DateTime.Now.AddDays(-1);
                Response.Cookies.Add(aCookie);
            }
        }
        Response.Redirect(Request.Path);
    }

       
</script>