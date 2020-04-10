% changed functions which are outdated
function [x, y, dt] = simple_polygon(numSides)

    if numSides < 3
        x = [];
        y = [];
        dt = [];
        return
    end

    oldState = warning('off', 'MATLAB:TriRep:PtsNotInTriWarnId');

    fudge = ceil(numSides/10);
    x = rand(numSides+fudge, 1);
    y = rand(numSides+fudge, 1);
% Igual
%     x = [0.9300,0.3990,0.0474,0.3424,0.7360,0.7947,0.5449]';
%     y = [0.6862,0.8936,0.0548,0.3037,0.0462,0.1955,0.7202]';
% Menor
    x = [0.6801,0.3672,0.2393,0.3424,0.8669,0.4068]';
    y = [0.1126,0.4438,0.3002,0.4014,0.8334,0.4036]';
% Mayor
%     x = [0.0868,0.4294,0.2573,0.2976,0.4249,0.1192]';
%     y = [0.4951,0.7064,0.2436,0.7851,0.0741,0.3939]';
    
%     dt1 = DelaunayTri(x, y);
    dt = delaunayTriangulation(x, y);
    
    boundaryEdges = freeBoundary(dt);

    % Plot resulting triangulation, not really necessary  
    triplot(dt)
    pause;
    hold on
    plot(x(boundaryEdges),y(boundaryEdges),'-r','LineWidth',2)
    pause;
    
%     x(boundaryEdges),y(boundaryEdges)
    numEdges = size(boundaryEdges, 1)
    numSides
    while numEdges ~= numSides
        if numEdges > numSides
% Returns the simplices attached to the specified vertices
            triIndex = vertexAttachments(dt, boundaryEdges(:,1));
            triIndex = triIndex(randperm(numel(triIndex)));
            keep = (cellfun('size', triIndex, 2) ~= 1);
            warning('mayor');
        end
        if (numEdges < numSides) || all(keep)
% Returns the simplices attached to the specified edges
            triIndex = edgeAttachments(dt, boundaryEdges);
            triIndex = triIndex(randperm(numel(triIndex)));
            triPoints = dt([triIndex{:}], :);
            keep = all(ismember(triPoints, boundaryEdges(:,1)), 2);
            warning('menor');
        end
        if all(keep)
            warning('Couldn''t achieve desired number of sides!');
            break
        end
%         triPoints = dt.Triangulation;
%         dt1 = TriRep(triPoints, x, y);
        triPoints = dt.ConnectivityList;
        triPoints(triIndex{find(~keep, 1)}, :) = [];
        dt = triangulation(triPoints, x, y);
        boundaryEdges = freeBoundary(dt);
        numEdges = size(boundaryEdges, 1);
    end

    boundaryEdges = [boundaryEdges(:,1); boundaryEdges(1,1)];
%     x = dt.X(boundaryEdges, 1);
%     y = dt.X(boundaryEdges, 2);
    x = dt.Points(boundaryEdges, 1);   
    y = dt.Points(boundaryEdges, 2);

    warning(oldState);

end
